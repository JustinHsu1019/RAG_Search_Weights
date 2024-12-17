import os
import pandas as pd
import ast

# 路徑設定
input_file = 'result/test_1210/result_185_top3.xlsx'
output_file = 'result/test_1210/result_185_top1.xlsx'

# 讀取 Excel 檔案
df = pd.read_excel(input_file)

# 出現列句的凡是 list 的格子只保留第一個值
def keep_top1(value):
    try:
        # 將值轉成列表
        parsed_list = ast.literal_eval(value)
        if isinstance(parsed_list, list) and len(parsed_list) > 0:
            return [parsed_list[0]]  # 保留第一個元素
    except (ValueError, SyntaxError):
        pass
    return value  # 如果不是列表或發生錯誤就保持原值

# 重新處理整個 DataFrame
df = df.applymap(keep_top1)

# 計算行數
total_rows_before = len(df)

# 儲存新檔案
df.to_excel(output_file, index=False)

# 列印結果
print(f"原始檔案行數: {total_rows_before}")
print(f"新的檔案行數: {total_rows_before}")
print(f"新的 Excel 檔案已儲存在: {output_file}")
