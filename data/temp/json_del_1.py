import json

# 讀取 JSON 檔案
def remove_unwanted_tags(file_path, output_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 篩選掉 tagone 為指定值的項目
        filtered_data = [item for item in data if item["tagone"] not in [
            "questionWithKeyword", "questionWithSynonym", "questionWithKeywordAndSynonym"
        ]]

        # 將過濾後的結果寫回新檔案
        with open(output_path, 'w', encoding='utf-8') as outfile:
            json.dump(filtered_data, outfile, ensure_ascii=False, indent=4)

        print(f"過濾完成，結果已儲存至 {output_path}")

    except FileNotFoundError:
        print("無法找到指定的 JSON 檔案，請檢查路徑是否正確。")
    except json.JSONDecodeError:
        print("JSON 檔案格式錯誤，無法解析。")

# 輸入與輸出檔案路徑
input_file = "data/question.json"
output_file = "data/question_filtered.json"

remove_unwanted_tags(input_file, output_file)
