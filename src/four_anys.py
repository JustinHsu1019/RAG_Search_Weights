import pandas as pd
import ast

def clean_text(text):
    return str(text).replace('"', "").replace("\n", "").replace("\\n", "").replace("\\", "").strip()

def is_correct_result(results_str, correct_answer_id):
    if pd.isna(results_str):
        return False
    try:
        results_list = ast.literal_eval(str(results_str))
        return correct_answer_id in results_list
    except:
        return False

def analyze(file_path):
    df = pd.read_excel(file_path)

    # 預期檢索結果欄位列表
    ratios = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    retrieval_cols = [f"檢索結果_{r}" for r in ratios]

    condition1_qids = []
    condition2_qids = []
    condition3_qids = []
    condition4_qids = []

    for idx, row in df.iterrows():
        qid = row["QID"]
        correct_answer_id = clean_text(row["答案"])

        # 將此列各 ratio 的正確與否記錄下來
        correct_dict = {}
        for r in ratios:
            col = f"檢索結果_{r}"
            correct_dict[r] = is_correct_result(row[col], correct_answer_id)

        # Condition 1:
        # "1.0"錯 & 其他任一 ratio 有對
        if correct_dict[1.0] == False and any(correct_dict[r] for r in ratios if r != 1.0):
            condition1_qids.append(qid)

        # Condition 2:
        # "0.0"錯 & 其他任一 ratio 有對
        if correct_dict[0.0] == False and any(correct_dict[r] for r in ratios if r != 0.0):
            condition2_qids.append(qid)

        # Condition 3:
        # "1.0"錯
        # [0.9,0.8,0.7,0.6,0.5] 至少一個對
        # [0.4,0.3,0.2,0.1,0.0] 全部錯
        if (correct_dict[1.0] == False and
            any(correct_dict[r] for r in [0.9,0.8,0.7,0.6,0.5]) and
            all(correct_dict[r] == False for r in [0.4,0.3,0.2,0.1,0.0])):
            condition3_qids.append(qid)

        # Condition 4:
        # "0.0"錯
        # [1.0,0.9,0.8,0.7,0.6] 全部錯
        # [0.5,0.4,0.3,0.2,0.1] 至少一個對
        if (correct_dict[0.0] == False and
            all(correct_dict[r] == False for r in [1.0,0.9,0.8,0.7,0.6]) and
            any(correct_dict[r] for r in [0.5,0.4,0.3,0.2,0.1])):
            condition4_qids.append(qid)

    # 將結果寫入四個 txt 檔
    with open("condition1.txt", "w", encoding="utf-8") as f:
        for q in condition1_qids:
            f.write(q + "\n")

    with open("condition2.txt", "w", encoding="utf-8") as f:
        for q in condition2_qids:
            f.write(q + "\n")

    with open("condition3.txt", "w", encoding="utf-8") as f:
        for q in condition3_qids:
            f.write(q + "\n")

    with open("condition4.txt", "w", encoding="utf-8") as f:
        for q in condition4_qids:
            f.write(q + "\n")


if __name__ == "__main__":
    analyze("result/test_1210/testresult_185.xlsx")
