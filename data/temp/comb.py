import os
import pandas as pd

# 設定路徑和輸出檔案路徑
folder_path = 'result/test_1210'
output_file = 'result/test_1210/merged_result.xlsx'

# 列出所有 Excel 檔案
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]

# 初始化結果列表
all_dataframes = []
file_row_counts = {}

# 讀取每個 Excel 檔案並組合
for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    row_count = len(df)
    file_row_counts[file] = row_count  # 記錄個別的欄位數
    all_dataframes.append(df)

# 合併所有檔案
merged_df = pd.concat(all_dataframes, ignore_index=True)

# 記錄合併後的欄位數
total_rows = len(merged_df)

# 存儲合併後的檔案
merged_df.to_excel(output_file, index=False)

# 列印結果
print("\n個別 Excel 檔案的列數:")
for file, count in file_row_counts.items():
    print(f"{file}: {count} 列")

print(f"\n合併後的檔案欄位數: {total_rows}")
print(f"新的 Excel 檔案已儲存在: {output_file}")
