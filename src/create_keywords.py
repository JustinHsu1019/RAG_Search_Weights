import json
import os
import re

def process_remaining_questions(input_file, output_file):
    """
    處理問題 JSON 檔案，篩選出 tagone 為 "questionWithKeyword" 的項目，
    並提取出 question 欄位中基於規則抓取的剩餘部分生成新的 JSON 檔案。

    :param input_file: 原始 JSON 檔案路徑
    :param output_file: 生成的 JSON 檔案路徑
    """

    # 檢查輸入檔案是否存在
    if not os.path.exists(input_file):
        print(f"輸入檔案 {input_file} 不存在。")
        return

    # 讀取原始 JSON 資料
    with open(input_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"讀取 JSON 檔案時發生錯誤: {e}")
            return

    # 篩選出 tagone 為 "questionWithKeyword" 的項目
    filtered = [item for item in data if item.get('tagone') == 'questionWithSynonym']

    new_data = []
    # 使用計數器來生成唯一的索引
    for idx, item in enumerate(filtered, start=1):
        parentqid = item.get('parentqid', '').strip()
        question = item.get('question', '').strip()

        if not parentqid or not question:
            print(f"項目缺少 parentqid 或 question，跳過: {item}")
            continue

        # 使用正則表達式將 "第 x 條" 轉換為 "第x條"，忽略 x 前後的空格
        question_processed = re.sub(r'第\s*(\d+)\s*條', r'第\1條', question)

        # 使用空格分割問題，取剩餘部分
        remaining_part = ' '.join(question_processed.split(' ')[1:]).strip()

        if not remaining_part:
            print(f"無剩餘部分，跳過: {item}")
            continue

        # 生成新的 qid，格式為 parentqid_keywordpart_X
        new_qid = f"{parentqid}_synonympart_{idx}"

        # 建立新的項目
        new_item = {
            "qid": new_qid,
            "parentqid": parentqid,
            "tagone": "synonympart",
            "tagtwo": "",
            "question": remaining_part
        }

        new_data.append(new_item)

    # 確保輸出目錄存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 將新的資料寫入 JSON 檔案，確保中文不被轉碼
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

    print(f"成功生成 {output_file}，共處理 {len(new_data)} 筆資料。")

if __name__ == "__main__":
    input_path = 'data/question.json'
    output_path = 'data/question_synonym.json'
    process_remaining_questions(input_path, output_path)
