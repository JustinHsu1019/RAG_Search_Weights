import pandas as pd
import ast


def clean_text(text):
    return str(text).replace('"', "").replace("\n", "").replace("\\n", "").replace("\\", "").replace(" ", "")


def calculate_accuracy(file_path):
    # 讀取新的測試結果 Excel 檔案
    df = pd.read_excel(file_path)
    total_questions = len(df) // 11  # 每題對應 11 行檢索比例
    accuracies = {round(x * 0.1, 1): 0 for x in range(10, -1, -1)}
    skipped_questions = 0  # 統計未能處理的題目數量

    for i in range(total_questions):
        # 提取正確答案
        correct_answer_id = clean_text(df.iloc[i * 11]["答案"])

        for alpha_idx, alpha in enumerate([round(x * 0.1, 1) for x in range(10, -1, -1)]):
            results_str = df.iloc[i * 11 + alpha_idx][f"檢索結果_{alpha}"]
            try:
                # 將字串解析為列表，例如 "['Q1']" -> ["Q1"]
                results_list = ast.literal_eval(results_str)
            except Exception as e:
                print(f"解析檢索結果字串時出錯，索引 {i * 11 + alpha_idx}：{e}")
                skipped_questions += 1
                continue

            # 比對正確答案是否出現在檢索結果中
            if correct_answer_id in results_list:
                accuracies[alpha] += 1

    # 計算有效題目總數（扣除跳過的題目）
    effective_total_questions = total_questions - skipped_questions
    if effective_total_questions == 0:
        print("沒有有效的題目被處理。")
        return accuracies

    # 計算每個 alpha 的準確率
    for alpha in accuracies:
        accuracies[alpha] = accuracies[alpha] / effective_total_questions

    return accuracies


if __name__ == "__main__":
    accuracies = calculate_accuracy("result/test_1210/testresult_185.xlsx")

    for alpha, accuracy in accuracies.items():
        print(f"檢索結果_{alpha} 準確率: {accuracy:.2%}")
