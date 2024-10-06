""" 測試結果 """
# 檢索結果_1.0 準確率: 70.00%
# 檢索結果_0.9 準確率: 73.33%
# 檢索結果_0.8 準確率: 83.33%
# 檢索結果_0.7 準確率: 83.33%
# 檢索結果_0.6 準確率: 83.33%
# 檢索結果_0.5 準確率: 80.00%
# 檢索結果_0.4 準確率: 86.67%
# 檢索結果_0.3 準確率: 83.33%
# 檢索結果_0.2 準確率: 83.33%
# 檢索結果_0.1 準確率: 83.33%
import pandas as pd
import ast

def clean_text(text):
    return text.replace('"', '').replace('\n', '').replace('\\n', '').replace('\\', '').replace(' ', '')

def calculate_accuracy(file_path):
    df = pd.read_excel(file_path)
    total_questions = len(df) // 10
    accuracies = {round(x * 0.1, 1): 0 for x in range(10, 0, -1)}

    for i in range(total_questions):
        correct_answer = clean_text(df.iloc[i * 10]['答案'])
        for alpha_idx, alpha in enumerate([round(x * 0.1, 1) for x in range(10, 0, -1)]):
            results_str = df.iloc[i * 10 + alpha_idx][f'檢索結果_{alpha}']
            results_list = ast.literal_eval(results_str)
            results_cleaned = [clean_text(result) for result in results_list]
            if correct_answer in results_cleaned:
                accuracies[alpha] += 1

    for alpha in accuracies:
        accuracies[alpha] = accuracies[alpha] / total_questions

    return accuracies

accuracies = calculate_accuracy('data/第二次試驗/【測試結果】_60題.xlsx')

for alpha, accuracy in accuracies.items():
    print(f'檢索結果_{alpha} 準確率: {accuracy:.2%}')
