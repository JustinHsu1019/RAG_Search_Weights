import json
import sys
import os
import openai

from small_keywords import small_key

# 載入設定檔與 Logger (依實際情況調整)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils.config_log as config_log
config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)
openai.api_key = config.get("OpenAI", "api_key")

def call_gpt(prompt, system_prompt=""):
    """Calls the OpenAI API with the given prompt and returns the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return None

if __name__ == "__main__":
    original_file = 'data/question_original.json'
    keyword_file = 'data/question_keyword.json'
    output_file = 'data/question_smallkeyword.json'

    # 1. 建立 parentqid 與 originalquestion 的映射
    with open(original_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    parent_to_original = {}
    for item in original_data:
        pqid = item.get('parentqid', '')
        question = item.get('question', '')
        # 只存 originalquestion tagone 的問題
        if item.get('tagone', '') == 'originalquestion':
            parent_to_original[pqid] = question

    # 2. 處理 question_keyword 資料
    with open(keyword_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output_data = []
    for item in data:
        qid = item['qid']
        parentqid = item.get('parentqid', '')
        tagone = item.get('tagone', '')
        tagtwo = item.get('tagtwo', '')
        keywords_question = item.get('question', '')

        original_question = parent_to_original.get(parentqid, '')

        if not original_question:
            original_question = keywords_question
            print(f"Error: For qid:{qid} No original question found.")

        # 產生 prompt
        prompt = small_key(original_question, keywords_question)
        small_keywords = call_gpt(prompt)
        print(f"small_keywords QID:{qid} = {small_keywords}")

        if not small_keywords:
            small_keywords = keywords_question
            print(f"Error: For qid:{qid} No small keywords found.")

        # 修改 qid 與 tagone
        new_qid = qid.replace("keywordpart", "smallkeywordpart")
        new_tagone = "smallkeywordpart"

        new_item = {
            "qid": new_qid,
            "parentqid": parentqid,
            "tagone": new_tagone,
            "tagtwo": tagtwo,
            "question": small_keywords
        }

        output_data.append(new_item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("Data transformed and saved to", output_file)
