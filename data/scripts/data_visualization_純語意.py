import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

file_path = 'data/第一次試驗/【測試結果】_60題_含準確率.xlsx'
sheets_weights = {
    'alpha 1.0': '10:0',
    'alpha 0.9': '9:1',
    'alpha 0.8': '8:2',
    'alpha 0.7': '7:3',
    'alpha 0.6': '6:4',
    'alpha 0.5': '5:5',
    'alpha 0.4': '4:6',
    'alpha 0.3': '3:7',
    'alpha 0.2': '2:8',
    'alpha 0.1': '1:9'
}
weights = []
retrieval_accuracy = []
answer_accuracy = []
for sheet, weight in sheets_weights.items():
    df = pd.read_excel(file_path, sheet_name=sheet)

    retrieval_col = '純語意_檢索準確率'
    answer_col = '純語意_答案準確率'

    if retrieval_col in df.columns and answer_col in df.columns:
        retrieval_value = df[retrieval_col].iloc[0]
        answer_value = df[answer_col].iloc[0]
        
        weights.append(weight)
        retrieval_accuracy.append(retrieval_value)
        answer_accuracy.append(answer_value)
    else:
        print(f"Columns '{retrieval_col}' or '{answer_col}' not found in sheet '{sheet}'")

data = {
    'Weights': weights,
    'Retrieval Accuracy': retrieval_accuracy,
    'Answer Accuracy': answer_accuracy
}
df = pd.DataFrame(data)

# 歸一化函數
def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

# 歸一化分數
df['Retrieval Accuracy (Normalized)'] = normalize(df['Retrieval Accuracy'])
df['Answer Accuracy (Normalized)'] = normalize(df['Answer Accuracy'])

# 計算綜合得分
df['Combined Score'] = 0.5 * df['Retrieval Accuracy (Normalized)'] + 0.5 * df['Answer Accuracy (Normalized)']

# 檢索準確性柱狀圖
plt.figure(figsize=(10, 6))
plt.bar(df['Weights'], df['Retrieval Accuracy'], color='skyblue')
plt.xlabel('Weights')
plt.ylabel('Retrieval Accuracy (%)')
plt.title('Retrieval Accuracy for Different Weight Configurations')
plt.savefig('data/第一次試驗/純語意_img/retrieval_accuracy.png')

# 答案準確性柱狀圖
plt.figure(figsize=(10, 6))
plt.bar(df['Weights'], df['Answer Accuracy'], color='lightgreen')
plt.xlabel('Weights')
plt.ylabel('Answer Accuracy (%)')
plt.title('Answer Accuracy for Different Weight Configurations')
plt.savefig('data/第一次試驗/純語意_img/answer_accuracy.png')

# 混合圖表
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df['Weights'], df['Retrieval Accuracy'], color='skyblue', label='Retrieval Accuracy')
ax.bar(df['Weights'], df['Answer Accuracy'], color='lightgreen', label='Answer Accuracy', alpha=0.7)
ax.set_xlabel('Weights')
ax.set_ylabel('Accuracy (%)')
ax.set_title('Comparison of Retrieval and Answer Accuracy')
ax.legend()
plt.savefig('data/第一次試驗/純語意_img/comparison_accuracy.png')

# 趨勢圖
plt.figure(figsize=(10, 6))
plt.plot(df['Weights'], df['Retrieval Accuracy'], marker='o', label='Retrieval Accuracy', color='skyblue')
plt.plot(df['Weights'], df['Answer Accuracy'], marker='o', label='Answer Accuracy', color='lightgreen')
plt.xlabel('Weights')
plt.ylabel('Accuracy (%)')
plt.title('Trend of Retrieval and Answer Accuracy')
plt.legend()
plt.savefig('data/第一次試驗/純語意_img/trend_accuracy.png')

# 綜合排序圖表
plt.figure(figsize=(10, 6))
plt.bar(df['Weights'], df['Combined Score'], color='lightcoral')
plt.xlabel('Weights')
plt.ylabel('Combined Score')
plt.title('Combined Score for Different Weight Configurations')
plt.savefig('data/第一次試驗/純語意_img/combined_score.png')
