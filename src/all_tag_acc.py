import pandas as pd
import ast
import json

def clean_text(text):
    return str(text).replace('"', "").replace("\n", "").replace("\\n", "").replace("\\", "").strip()

def calculate_accuracy_by_tagone(file_path, question_json_path):
    # 從 question.json 中讀取並建立 qid 到 tagone 的對照表
    with open(question_json_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    qid_to_tagone = {item['qid']: item['tagone'] for item in questions_data}

    # 讀取結果的 Excel 檔案
    df = pd.read_excel(file_path)

    # 找出所有檢索結果的欄位名稱(通常是檢索結果_x.x)
    retrieval_columns = [col for col in df.columns if col.startswith("檢索結果_")]

    # 用來記錄各 tagone 的統計 {tagone: {"correct":int, "total":int}}
    tagone_stats = {}

    for idx, row in df.iterrows():
        qid = row["QID"]
        correct_answer_id = clean_text(row["答案"])

        # 取得該行 QID 對應的 tagone
        if qid not in qid_to_tagone:
            # 若在 question.json 中找不到對應的 qid, 則此列可能跳過或歸類為未知
            tagone = "UnknownTag"
        else:
            tagone = qid_to_tagone[qid]

        # 初始化 tagone 的計算字典
        if tagone not in tagone_stats:
            tagone_stats[tagone] = {"correct": 0, "total": 0}

        # 檢查此行的所有檢索結果欄位
        found_correct = False
        for col in retrieval_columns:
            results_str = row[col]
            if pd.isna(results_str):
                continue
            try:
                results_list = ast.literal_eval(str(results_str))
            except:
                # 若解析失敗，則略過此欄
                continue

            if correct_answer_id in results_list:
                found_correct = True
                break
        
        # 累積計算
        tagone_stats[tagone]["total"] += 1
        if found_correct:
            tagone_stats[tagone]["correct"] += 1

    # 計算每個 tagone 的準確率
    tagone_accuracies = {}
    for tagone, stats in tagone_stats.items():
        total = stats["total"]
        correct = stats["correct"]
        accuracy = correct / total if total > 0 else 0
        tagone_accuracies[tagone] = accuracy

    return tagone_accuracies


if __name__ == "__main__":
    # 假設您的檔案路徑如下
    result = calculate_accuracy_by_tagone("result/test_1210/result_185_top1.xlsx", "data/question.json")
    for tagone, acc in result.items():
        print(f"Tagone: {tagone}, 準確率: {acc:.2%}")
