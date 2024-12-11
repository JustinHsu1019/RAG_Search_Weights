import pandas as pd
import json
import ast
import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

import jieba
from nltk.corpus import stopwords
import nltk

# 確保目標資料夾存在
os.makedirs('result/clustering', exist_ok=True)

# 下載 NLTK 中文停用詞（如果尚未下載）
nltk.download('stopwords')

print("1. 讀取並整合資料")

# 1. 讀取 Excel 檔案
excel_file_path = 'result/test_1210/testresult_185_top3.xlsx'
df = pd.read_excel(excel_file_path)

print(f"Total records: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# 2. 讀取 JSON 檔案
json_file_path = 'data/question.json'
with open(json_file_path, 'r', encoding='utf-8') as f:
    questions = json.load(f)

# 將 JSON 資料轉換為 DataFrame
questions_df = pd.DataFrame(questions)

print(f"Number of questions read: {len(questions_df)}")
print(questions_df.head())

# 3. 選取必要的欄位並重命名
questions_df = questions_df[['qid', 'tagone']]
questions_df = questions_df.rename(columns={'qid': 'QID'})

print("Processed questions data:")
print(questions_df.head())

# 4. 合併資料
merged_df = df.merge(questions_df, on='QID', how='left')

print("Merged data preview:")
print(merged_df.head())

# 檢查是否有未匹配的 QID
unmatched = merged_df['tagone'].isnull().sum()
if unmatched > 0:
    print(f"There are {unmatched} QIDs without corresponding tagone in JSON.")
    # 填補未匹配的 tagone 為 'Unknown'
    merged_df['tagone'] = merged_df['tagone'].fillna('Unknown')

# 儲存合併後的資料（可選）
merged_output_path = 'result/clustering/merged_data.xlsx'
merged_df.to_excel(merged_output_path, index=False)
print(f"Merged data saved to '{merged_output_path}'")

print("\n2. 文本預處理與向量化")

# 定義停用詞
# 使用 NLTK 的中文停用詞列表或自定義
# 這裡假設使用一個中文停用詞文件，您需要提供該文件
# 例如，假設停用詞文件為 'chinese_stopwords.txt'
# 您可以從網上下載中文停用詞列表，如[中文停用詞表](https://github.com/goto456/stopwords/blob/master/stopwords-master/cn_stopwords.txt)

stopwords_path = 'data/chinese_stopwords.txt'  # 修改為您的停用詞文件路徑
if os.path.exists(stopwords_path):
    with open(stopwords_path, 'r', encoding='utf-8') as f:
        chinese_stopwords = set(f.read().splitlines())
else:
    # 如果沒有停用詞文件，可以使用 NLTK 的英文停用詞，作為替代
    # 或者定義一個簡單的中文停用詞列表
    print(f"Stopwords file '{stopwords_path}' not found. Using default empty stopwords.")
    chinese_stopwords = set()

# 如果您使用的是 jieba，可以將停用詞應用於分詞後的結果
def preprocess_text(text):
    # 分詞
    tokens = jieba.lcut(text)
    # 去除停用詞
    tokens = [word for word in tokens if word not in chinese_stopwords and word.strip()]
    # 重組文本
    return ' '.join(tokens)

# 應用預處理
merged_df['processed_question'] = merged_df['問題'].apply(preprocess_text)

print("Text preprocessing completed.")
print(merged_df[['問題', 'processed_question']].head())

# 2. 向量化：使用 TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
tfidf_matrix = vectorizer.fit_transform(merged_df['processed_question'])

print(f"TF-IDF matrix shape: {tfidf_matrix.shape}")

print("\n3. 應用 LSA 進行降維")

# 1. 應用 LSA（TruncatedSVD）
n_components = 100  # 可以根據需求調整
lsa = TruncatedSVD(n_components=n_components, random_state=42)
lsa_matrix = lsa.fit_transform(tfidf_matrix)

print(f"LSA reduced matrix shape: {lsa_matrix.shape}")

print("\n4. 聚類分析")

# 1. 選擇聚類數量（固定為7類）
optimal_k = 7
print(f"Setting number of clusters to {optimal_k} to match 'tagone' categories.")

# 2. 執行 K-Means 聚類
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
kmeans.fit(lsa_matrix)
labels = kmeans.labels_

# 將聚類標籤加入 DataFrame
merged_df['Cluster'] = labels

print("Clustering completed. Cluster labels added to data.")
print(merged_df[['QID', 'Cluster']].head())

print("\n5. 分析聚類結果與 tagone 的相關性")

# 1. 生成交叉表（Contingency Table）
contingency_table = pd.crosstab(merged_df['Cluster'], merged_df['tagone'], margins=True, normalize='index')

print("Cluster vs. Tagone Contingency Table (Proportions):")
print(contingency_table)

# 2. 繪製熱力圖
plt.figure(figsize=(12, 8))
sns.heatmap(contingency_table, annot=True, fmt=".2f", cmap='YlGnBu')
plt.title('Cluster vs. Tagone Heatmap')
plt.xlabel('Tagone')
plt.ylabel('Cluster')
plt.tight_layout()
plt.savefig('result/clustering/cluster_tagone_heatmap.png')
plt.show()
print("Cluster vs. Tagone heatmap saved to 'result/clustering/cluster_tagone_heatmap.png'")

# 3. 繪製每個 Cluster 中各 tagone 的分佈（堆疊柱狀圖）
plt.figure(figsize=(14, 8))
merged_df.groupby(['Cluster', 'tagone']).size().unstack(fill_value=0).plot(
    kind='bar', 
    stacked=True, 
    colormap='tab20', 
    figsize=(14,8)
)
plt.title('Distribution of Tagone within Each Cluster')
plt.xlabel('Cluster')
plt.ylabel('Count')
plt.legend(title='Tagone', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('result/clustering/cluster_tagone_stacked_bar.png')
plt.show()
print("Distribution of Tagone within Each Cluster saved to 'result/clustering/cluster_tagone_stacked_bar.png'")

print("\n6. 將聚類結果與 tagone 儲存至 Excel")

final_output_path = 'result/clustering/clustered_qids_with_tagone.xlsx'
merged_df.to_excel(final_output_path, index=False)
print(f"Final clustering results saved to '{final_output_path}'")

print("\n7. 進一步的視覺化（可選）")

# 1. 使用 t-SNE 將高維資料降維至 2D 進行視覺化
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=3000)
tsne_results = tsne.fit_transform(lsa_matrix)

merged_df['TSNE1'] = tsne_results[:, 0]
merged_df['TSNE2'] = tsne_results[:, 1]

plt.figure(figsize=(12, 8))
sns.scatterplot(data=merged_df, x='TSNE1', y='TSNE2', hue='Cluster', palette='tab20', alpha=0.6)
plt.title('t-SNE Visualization of Clusters')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('result/clustering/tsne_clusters_visualization.png')
plt.show()
print("t-SNE cluster visualization saved to 'result/clustering/tsne_clusters_visualization.png'")

# 2. 保存 t-SNE 資料（可選）
tsne_output_path = 'result/clustering/qid_with_tsne.xlsx'
merged_df.to_excel(tsne_output_path, index=False)
print(f"t-SNE data saved to '{tsne_output_path}'")
