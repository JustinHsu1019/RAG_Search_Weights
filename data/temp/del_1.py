import pandas as pd
import json

# 讀取 Excel 檔案
excel_path = 'result/test_1210/testresult_185_top3.xlsx'
dataframe = pd.read_excel(excel_path)

# 讀取 JSON 檔案
json_path = 'data/question.json'
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 判斷 tagone 是否符合條件 ("questionWithKeyword", "questionWithSynonym", "questionWithKeywordAndSynonym")
filter_tags = {"questionWithKeyword", "questionWithSynonym", "questionWithKeywordAndSynonym"}
filter_qids = {item['qid'] for item in json_data if item['tagone'] in filter_tags}
print(filter_qids)

# 列印結果
total_rows = len(dataframe)
print(f"Excel 原始總行數: {total_rows}")

# 刪除符合條件的 QID
filtered_df = dataframe[~dataframe['QID'].isin(filter_qids)]
deleted_rows = total_rows - len(filtered_df)

# 存檔到新 Excel 檔案
output_path = 'result/test_1210/filtered_testresult.xlsx'
filtered_df.to_excel(output_path, index=False)

# 列印結果
print(f"刪除行數: {deleted_rows}")
print(f"剩余行數: {len(filtered_df)}")
print(f"新的 Excel 檔案已儲存在: {output_path}")
