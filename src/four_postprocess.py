# TODO: 把 Any Correct 改成 "峰值：Ratio 多少、正確率有多高", 然後把 Specific Condition 這個欄位刪掉
import pandas as pd
import ast
import json

def clean_text(text):
    """清理文本，移除不必要的字符並去除前後空白。"""
    return str(text).replace('"', "").replace("\n", "").replace("\\n", "").replace("\\", "").strip()

def load_qid_to_tagone(json_path):
    """讀取 question.json 並建立 QID 到 tagone 的對照表。"""
    with open(json_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    qid_to_tagone = {item['qid']: item['tagone'] for item in questions_data}
    return qid_to_tagone

def is_correct_result(results_str, correct_answer_id):
    """判斷檢索結果中是否包含正確答案。"""
    if pd.isna(results_str):
        return False
    try:
        results_list = ast.literal_eval(str(results_str))
        return correct_answer_id in results_list
    except:
        return False

def analyze(file_path, question_json_path):
    """進行分析並輸出結構化的報告。"""
    # 載入 QID 到 tagone 的對照表
    qid_to_tagone = load_qid_to_tagone(question_json_path)
    
    # 讀取 Excel 檔案
    df = pd.read_excel(file_path)
    
    # 定義所有 ratio
    ratios = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    retrieval_cols = [f"檢索結果_{r}" for r in ratios]
    
    # 初始化 tagone 的統計資料結構
    tag_stats = {}
    
    for idx, row in df.iterrows():
        qid = row["QID"]
        tagone = qid_to_tagone.get(qid, "UnknownTag")
        correct_answer_id = clean_text(row["答案"])
        
        # 初始化 tagone 的計數
        if tagone not in tag_stats:
            tag_stats[tagone] = {
                "total_questions": 0,
                "1.0_wrong": 0,
                "1.0_wrong_any_correct": 0,
                "1.0_wrong_specific_condition": 0,
                "0.0_wrong": 0,
                "0.0_wrong_any_correct": 0,
                "0.0_wrong_specific_condition": 0
            }
        
        tag_stats[tagone]["total_questions"] += 1
        
        # 檢查各 ratio 的正確與否
        correct_dict = {}
        for r in ratios:
            col = f"檢索結果_{r}"
            correct_dict[r] = is_correct_result(row[col], correct_answer_id)
        
        # 分析 '1.0' 條件
        if not correct_dict[1.0]:
            tag_stats[tagone]["1.0_wrong"] += 1
            if any(correct_dict[r] for r in ratios if r != 1.0):
                tag_stats[tagone]["1.0_wrong_any_correct"] += 1
            # Condition3: '1.0' 錯，0.9-0.5 有一個對，0.4-0.0 全錯
            condition3 = (
                not correct_dict[1.0] and
                any(correct_dict[r] for r in [0.9, 0.8, 0.7, 0.6, 0.5]) and
                all(not correct_dict[r] for r in [0.4, 0.3, 0.2, 0.1, 0.0])
            )
            if condition3:
                tag_stats[tagone]["1.0_wrong_specific_condition"] += 1
        
        # 分析 '0.0' 條件
        if not correct_dict[0.0]:
            tag_stats[tagone]["0.0_wrong"] += 1
            if any(correct_dict[r] for r in ratios if r != 0.0):
                tag_stats[tagone]["0.0_wrong_any_correct"] += 1
            # Condition4: '0.0' 錯，1.0-0.6 全錯，0.5-0.1 有一個對
            condition4 = (
                not correct_dict[0.0] and
                all(not correct_dict[r] for r in [1.0, 0.9, 0.8, 0.7, 0.6]) and
                any(correct_dict[r] for r in [0.5, 0.4, 0.3, 0.2, 0.1])
            )
            if condition4:
                tag_stats[tagone]["0.0_wrong_specific_condition"] += 1
    
    # 定義欄位標題
    headers = [
        "Tagone",
        "Total Questions",
        "1.0 Wrong %",
        "1.0 Wrong & Any Correct %",
        "1.0 Wrong & Specific Condition %",
        "0.0 Wrong %",
        "0.0 Wrong & Any Correct %",
        "0.0 Wrong & Specific Condition %"
    ]
    
    # 設定每欄的寬度
    col_widths = [30, 18, 15, 25, 30, 15, 25, 30]
    
    # 建立格式化字串
    header_fmt = "".join([f"{{:<{w}}}" for w in col_widths])
    row_fmt = "".join([f"{{:<{w}}}" for w in col_widths])
    
    # 打印標題
    print(header_fmt.format(*headers))
    print("-" * sum(col_widths))
    
    # 打印每個 tag 的統計數據
    for tag, stats in sorted(tag_stats.items(), key=lambda x: x[0]):
        total = stats["total_questions"]
        
        # 計算百分比
        p_1_wrong = (stats["1.0_wrong"] / total * 100) if total > 0 else 0
        p_1_wrong_any = (stats["1.0_wrong_any_correct"] / total * 100) if total > 0 else 0
        p_1_wrong_cond3 = (stats["1.0_wrong_specific_condition"] / total * 100) if total > 0 else 0
        p_0_wrong = (stats["0.0_wrong"] / total * 100) if total > 0 else 0
        p_0_wrong_any = (stats["0.0_wrong_any_correct"] / total * 100) if total > 0 else 0
        p_0_wrong_cond4 = (stats["0.0_wrong_specific_condition"] / total * 100) if total > 0 else 0
        
        # 準備行資料，僅包含百分比
        row = [
            tag,
            total,
            f"{p_1_wrong:.2f}%",
            f"{p_1_wrong_any:.2f}%",
            f"{p_1_wrong_cond3:.2f}%",
            f"{p_0_wrong:.2f}%",
            f"{p_0_wrong_any:.2f}%",
            f"{p_0_wrong_cond4:.2f}%"
        ]
        
        print(row_fmt.format(*row))
    
    # 如果需要將結果保存到檔案中，可以取消以下註解
    # with open("analysis_report_structured.txt", "w", encoding="utf-8") as f:
    #     f.write(header_fmt.format(*headers) + "\n")
    #     f.write("-" * sum(col_widths) + "\n")
    #     for tag, stats in sorted(tag_stats.items(), key=lambda x: x[0]):
    #         total = stats["total_questions"]
    #         # 計算百分比
    #         p_1_wrong = (stats["1.0_wrong"] / total * 100) if total > 0 else 0
    #         p_1_wrong_any = (stats["1.0_wrong_any_correct"] / total * 100) if total > 0 else 0
    #         p_1_wrong_cond3 = (stats["1.0_wrong_specific_condition"] / total * 100) if total > 0 else 0
    #         p_0_wrong = (stats["0.0_wrong"] / total * 100) if total > 0 else 0
    #         p_0_wrong_any = (stats["0.0_wrong_any_correct"] / total * 100) if total > 0 else 0
    #         p_0_wrong_cond4 = (stats["0.0_wrong_specific_condition"] / total * 100) if total > 0 else 0
    #         
    #         # 準備行資料，僅包含百分比
    #         row = [
    #             tag,
    #             total,
    #             f"{p_1_wrong:.2f}%",
    #             f"{p_1_wrong_any:.2f}%",
    #             f"{p_1_wrong_cond3:.2f}%",
    #             f"{p_0_wrong:.2f}%",
    #             f"{p_0_wrong_any:.2f}%",
    #             f"{p_0_wrong_cond4:.2f}%"
    #         ]
    #         
    #         f.write(row_fmt.format(*row) + "\n")

if __name__ == "__main__":
    # 調整為您的檔案路徑
    excel_file_path = "result/test_1210/testresult_185.xlsx"
    question_json_path = "data/question.json"
    analyze(excel_file_path, question_json_path)
