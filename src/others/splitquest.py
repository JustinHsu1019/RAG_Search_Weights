import pandas as pd


testkey_df = pd.read_excel("result/test_1006/testkey_3493.xlsx")
testresult_df = pd.read_excel("result/test_1006/CKIP/testresult_CKIP.xlsx")

merged_df = pd.merge(testkey_df, testresult_df, left_on="問題", right_on="問題")

keyword_num_avg = merged_df["keyword_num"].mean()
question_length_avg = merged_df["問題"].apply(len).mean()

multi_keyword_df = merged_df[merged_df["keyword_num"] > keyword_num_avg]
few_keyword_df = merged_df[merged_df["keyword_num"] <= keyword_num_avg]
long_sentence_df = merged_df[merged_df["問題"].apply(len) > question_length_avg]
short_sentence_df = merged_df[merged_df["問題"].apply(len) <= question_length_avg]

multi_keyword_df.to_excel("result/test_1006/問題分類/多關鍵字.xlsx", index=False)
few_keyword_df.to_excel("result/test_1006/問題分類/少關鍵字.xlsx", index=False)
long_sentence_df.to_excel("result/test_1006/問題分類/長語句.xlsx", index=False)
short_sentence_df.to_excel("result/test_1006/問題分類/短語句.xlsx", index=False)

print(
    "Excel files created: '多關鍵字.xlsx', '少關鍵字.xlsx', '長語句.xlsx', and '短語句.xlsx'."
)
