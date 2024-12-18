import json
import os

# 合併 data/ 路徑下的所有 question_ 開頭的 JSON 檔案
def merge_json_files(directory, output_file):
    merged_data = []
    file_stats = []

    try:
        # 瀏覽資料夾中的所有檔案
        for filename in os.listdir(directory):
            if filename.startswith("question_") and filename.endswith(".json"):
                file_path = os.path.join(directory, filename)

                # 讀取 JSON 檔案
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    merged_data.extend(data)

                    # 記錄檔名與筆數
                    file_stats.append({"filename": filename, "count": len(data)})

        # 將合併後的資料寫入輸出檔案
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(merged_data, outfile, ensure_ascii=False, indent=4)

        # 記錄合併檔案的資訊
        file_stats.append({"filename": output_file, "count": len(merged_data)})

        # 輸出結果
        for stat in file_stats:
            print(f"檔名: {stat['filename']}, 筆數: {stat['count']}")

    except Exception as e:
        print(f"發生錯誤: {e}")

# 設定資料夾與輸出檔案
input_directory = "data"
output_file = "data/question.json"

merge_json_files(input_directory, output_file)
