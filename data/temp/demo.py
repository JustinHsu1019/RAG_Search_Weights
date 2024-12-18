import json

# 讀取 question.json 檔案
def filter_and_merge_questions(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 篩選出 parentqid="Q1" 的資料
    filtered_data = [item for item in data if item.get("parentqid") == "Q1"]

    # 根據不同的 tagone 取出一筆資料
    unique_tagone = {}
    for item in filtered_data:
        tagone = item.get("tagone", "")
        if tagone and tagone not in unique_tagone:
            unique_tagone[tagone] = item

    # 將結果合併成新的 JSON 檔案
    result = list(unique_tagone.values())
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False, indent=4)

# 指定輸入和輸出檔案路徑
input_file = 'data/question.json'
output_file = 'data/filtered_question.json'

# 執行過濾與合併
filter_and_merge_questions(input_file, output_file)

print(f"Filtered data has been saved to {output_file}")
