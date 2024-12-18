import pandas as pd
import ast
import json

def clean_text(text):
    return str(text).replace('"', "").replace("\n", "").replace("\\n", "").replace("\\", "").strip()

def calculate_accuracy_by_tag_and_alpha(excel_file, question_json_file):
    # 從 question.json 中讀取並建立 qid 到 tagone 的對照表
    with open(question_json_file, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)
    qid_to_tagone = {item['qid']: item['tagone'] for item in questions_data}

    # 讀取結果的 Excel 檔案
    df = pd.read_excel(excel_file)

    # 定義 alpha 清單 (1.0, 0.9, 0.8, ..., 0.0)
    alphas = [round(x * 0.1, 1) for x in range(10, -1, -1)]

    # 計算總題數（假設每題對應 11 行）
    total_questions = len(df) // 11
    if total_questions == 0:
        print("沒有有效的題目可處理。")
        return {}

    # 建立資料結構： 
    # tag_alpha_stats[tag][alpha] = {"correct":int, "total":int}
    tag_alpha_stats = {}

    # 開始遍歷每個題目
    for i in range(total_questions):
        # 對應題目的第一列（i*11）取得 QID 和 正確答案
        qid = df.iloc[i * 11]["QID"]
        correct_answer_id = clean_text(df.iloc[i * 11]["答案"])
        tagone = qid_to_tagone.get(qid, "UnknownTag")

        # 初始化該 tag 的資料結構
        if tagone not in tag_alpha_stats:
            tag_alpha_stats[tagone] = {}
            for alpha in alphas:
                tag_alpha_stats[tagone][alpha] = {"correct":0, "total":0}

        # 對應 11 個 alpha 檢索結果列
        for alpha_idx, alpha in enumerate(alphas):
            results_str = df.iloc[i * 11 + alpha_idx].get(f"檢索結果_{alpha}", None)
            # 累計 total
            tag_alpha_stats[tagone][alpha]["total"] += 1

            if results_str is None or pd.isna(results_str):
                # 若沒有此欄位或內容 NaN，跳過，但已計 total
                continue

            try:
                results_list = ast.literal_eval(str(results_str))
            except Exception:
                # 若解析失敗，一樣計 total，但不計 correct
                continue

            # 檢查正確答案是否在結果中
            if correct_answer_id in results_list:
                tag_alpha_stats[tagone][alpha]["correct"] += 1

    # 計算每個 tag、每個 alpha 的準確率
    tag_list = sorted(tag_alpha_stats.keys())
    data = {}
    for alpha in alphas:
        data[alpha] = []
        for tag in tag_list:
            stats = tag_alpha_stats[tag][alpha]
            total = stats["total"]
            correct = stats["correct"]
            accuracy = correct / total if total > 0 else 0
            data[alpha].append(accuracy)

    result_df = pd.DataFrame(data, index=tag_list)
    result_df.index.name = "Tag"

    # 計算每個 tag 在所有 alpha 下的總體 (weighted) 準確率（加權平均）
    # 以及每個 alpha 在所有 tag 下的總體準確率
    # 同時計算整體的準確率
    # 需重新利用 tag_alpha_stats
    # 統計所有 tag, alpha 的 correct 和 total
    all_tags_alpha_total_correct = 0
    all_tags_alpha_total_total = 0

    # 計算行合計 (All Alpha) 與列合計 (All Tags)
    all_tags_row = []
    for tag in tag_list:
        tag_total_correct = 0
        tag_total_total = 0
        for alpha in alphas:
            c = tag_alpha_stats[tag][alpha]["correct"]
            t = tag_alpha_stats[tag][alpha]["total"]
            tag_total_correct += c
            tag_total_total += t
        tag_accuracy = tag_total_correct / tag_total_total if tag_total_total > 0 else 0
        all_tags_row.append(tag_accuracy)
        all_tags_alpha_total_correct += tag_total_correct
        all_tags_alpha_total_total += tag_total_total

    all_alpha_col = []
    for alpha in alphas:
        alpha_total_correct = 0
        alpha_total_total = 0
        for tag in tag_list:
            c = tag_alpha_stats[tag][alpha]["correct"]
            t = tag_alpha_stats[tag][alpha]["total"]
            alpha_total_correct += c
            alpha_total_total += t
        alpha_accuracy = alpha_total_correct / alpha_total_total if alpha_total_total > 0 else 0
        all_alpha_col.append(alpha_accuracy)

    overall_accuracy = all_tags_alpha_total_correct / all_tags_alpha_total_total if all_tags_alpha_total_total > 0 else 0

    # 將 All Alpha 加入欄位
    result_df["All Alpha"] = all_tags_row

    # 新增 All Tags 那一行
    all_tags_data = {alpha: acc for alpha, acc in zip(alphas, all_alpha_col)}
    all_tags_data["All Alpha"] = overall_accuracy
    all_tags_series = pd.Series(all_tags_data, name="All Tags")
    result_df = pd.concat([result_df, all_tags_series.to_frame().T])

    # 在 markdown 中標示每個 tag (每一 row，不包含 All Tags 那行) 中最大準確率
    # 不包括 "All Tags" 這一行
    # 不包括 "All Alpha" 這一欄
    def format_value(value):
        return f"{value*100:.2f}%"

    # 找出每行（tag）的最大值位置
    # 不包含 All Tags 行
    max_positions = {}
    for tag in tag_list:
        row_values = result_df.loc[tag, alphas].values
        max_val = row_values.max()
        # 找出所有等於 max_val 的 alpha（如果有多個同值，全部標粗）
        max_alphas = [alphas[i] for i, v in enumerate(row_values) if v == max_val]
        max_positions[tag] = max_alphas

    # 產出 markdown 表格
    # 表頭
    md = []
    all_cols = alphas + ["All Alpha"]

    md.append("| Tag | " + " | ".join(str(a) for a in all_cols) + " |")
    md.append("| ---- | " + " | ".join(["----"] * len(all_cols)) + " |")

    for tag in list(result_df.index):
        row_strs = []
        for alpha in all_cols:
            val = result_df.loc[tag, alpha]
            val_str = format_value(val)
            # 對一般的 tag 行，每個 alpha 如果是該行最大值，標粗體
            if tag in max_positions and alpha in max_positions[tag]:
                val_str = f"**{val_str}**"
            row_strs.append(val_str)
        md.append("| " + str(tag) + " | " + " | ".join(row_strs) + " |")

    markdown_table = "\n".join(md)
    return markdown_table


if __name__ == "__main__":
    excel_file = "result/test_1210/result_185_top1.xlsx"
    question_json_file = "data/question.json"
    markdown_table = calculate_accuracy_by_tag_and_alpha(excel_file, question_json_file)
    print(markdown_table)
