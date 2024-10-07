import pandas as pd
import ast


def clean_text(text):
    return (
        text.replace('"', "")
        .replace("\n", "")
        .replace("\\n", "")
        .replace("\\", "")
        .replace(" ", "")
    )


def calculate_accuracy(file_path):
    df = pd.read_excel(file_path)
    total_questions = len(df) // 11
    accuracies = {round(x * 0.1, 1): 0 for x in range(10, -1, -1)}

    for i in range(total_questions):
        correct_answer = clean_text(df.iloc[i * 11]["答案"])
        for alpha_idx, alpha in enumerate(
            [round(x * 0.1, 1) for x in range(10, -1, -1)]
        ):
            results_str = df.iloc[i * 11 + alpha_idx][f"檢索結果_{alpha}"]
            results_list = ast.literal_eval(results_str)
            results_cleaned = [clean_text(result) for result in results_list]
            if correct_answer in results_cleaned:
                accuracies[alpha] += 1

    for alpha in accuracies:
        accuracies[alpha] = accuracies[alpha] / total_questions

    return accuracies


accuracies = calculate_accuracy("result/test_1006/testresult_3493.xlsx")

for alpha, accuracy in accuracies.items():
    print(f"檢索結果_{alpha} 準確率: {accuracy:.2%}")
