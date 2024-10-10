import pandas as pd
import ast


def clean_text(text):
    return (
        str(text)
        .replace('"', "")
        .replace("\n", "")
        .replace("\\n", "")
        .replace("\\", "")
        .replace(" ", "")
    )


def calculate_accuracy(file_path):
    df = pd.read_excel(file_path)
    df_map = pd.read_excel("result/test_1006/context_mapping.xlsx")
    # 清洗 context_mapping.xlsx 中的 paragraph
    df_map["cleaned_paragraph"] = df_map["paragraph"].apply(clean_text)
    total_questions = len(df) // 11
    accuracies = {round(x * 0.1, 1): 0 for x in range(10, -1, -1)}
    skipped_questions = 0  # 用於統計未匹配到的答案數

    for i in range(total_questions):
        correct_answer_text = clean_text(df.iloc[i * 11]["答案"])
        # 在映射表中查找匹配的 id
        matched_rows = df_map[df_map["cleaned_paragraph"] == correct_answer_text]
        if not matched_rows.empty:
            correct_answer_id = matched_rows.iloc[0]["id"]
        else:
            print(f"未找到匹配的 id，問題索引：{i * 11}")
            skipped_questions += 1
            continue  # 跳過未匹配到的題目

        for alpha_idx, alpha in enumerate(
            [round(x * 0.1, 1) for x in range(10, -1, -1)]
        ):
            results_str = df.iloc[i * 11 + alpha_idx][f"檢索結果_{alpha}"]
            try:
                results_list = ast.literal_eval(results_str)
            except Exception as e:
                print(f"解析結果字符串時出錯，索引 {i * 11 + alpha_idx}：{e}")
                continue
            # 確保結果列表中的元素和 correct_answer_id 的類型一致
            results_list = [str(r) for r in results_list]  # 轉換為字符串
            correct_answer_id_str = str(correct_answer_id)
            if correct_answer_id_str in results_list:
                accuracies[alpha] += 1

    effective_total_questions = total_questions - skipped_questions
    if effective_total_questions == 0:
        print("沒有有效的題目被處理。")
        return accuracies

    for alpha in accuracies:
        accuracies[alpha] = accuracies[alpha] / effective_total_questions

    return accuracies


if __name__ == "__main__":
    accuracies = calculate_accuracy("result/test_1006/testresult_3493.xlsx")

    for alpha, accuracy in accuracies.items():
        print(f"檢索結果_{alpha} 準確率: {accuracy:.2%}")
