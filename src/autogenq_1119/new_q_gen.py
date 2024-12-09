import json
import sys
import os
import openai
from tqdm import tqdm
from langchain.text_splitter import RecursiveCharacterTextSplitter
from func_prompt import gene_q, change_str, condensed, keyword
from aug_prompt import questionSynonymChange, complexQuestionX2, complexQuestionX3, questionWithKnowledgeStyle, questionWithSynonym

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
            max_tokens=4096,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return None

def generate_questions(chunks):
    """Generates questions for each chunk."""
    questions = []
    for idx, chunk in enumerate(tqdm(chunks, desc="Generating original questions")):
        prompt = gene_q(chunk)
        question = call_gpt(prompt)
        # print(question)
        questions.append({
            "qid": f"Q{idx+1}",
            "parentqid": "",
            "tagone": "originalquestion",
            "tagtwo": "",
            "question": question,
            "chunk": chunk  # Store chunk for later use
        })
    return questions

def expand_question(base_qid, parent_qid, tagone, method_question):
    """Applies the 5 expansion steps to the method_question."""
    augmented_questions = []

    # 步驟1：原始問題（不做任何修改）
    augmented_questions.append({
        "qid": f"{base_qid}_{tagone}_1",
        "parentqid": parent_qid,
        "tagone": tagone,
        "tagtwo": "originalq",
        "question": method_question
    })

    # 步驟2：改變句型
    prompt = change_str(method_question)
    changed_structure = call_gpt(prompt)
    if changed_structure:
        augmented_questions.append({
            "qid": f"{base_qid}_{tagone}_2",
            "parentqid": parent_qid,
            "tagone": tagone,
            "tagtwo": "changeSentenceStructure",
            "question": changed_structure
        })

    # 步驟3：濃縮語意表達
    prompt = condensed(method_question)
    condensed_expression = call_gpt(prompt)
    if condensed_expression:
        augmented_questions.append({
            "qid": f"{base_qid}_{tagone}_3",
            "parentqid": parent_qid,
            "tagone": tagone,
            "tagtwo": "condensedSemanticExpression",
            "question": condensed_expression
        })

    # 步驟4：改變濃縮後問題的句型
    prompt = change_str(condensed_expression)
    condensed_changed = call_gpt(prompt)
    if condensed_changed:
        augmented_questions.append({
            "qid": f"{base_qid}_{tagone}_4",
            "parentqid": parent_qid,
            "tagone": tagone,
            "tagtwo": "condensedandChange",
            "question": condensed_changed
        })

    # 步驟5：提取關鍵字
    prompt = keyword(method_question)
    keywords = call_gpt(prompt)
    if keywords:
        augmented_questions.append({
            "qid": f"{base_qid}_{tagone}_5",
            "parentqid": parent_qid,
            "tagone": tagone,
            "tagtwo": "extractKeywords",
            "question": keywords
        })

    return augmented_questions

def augment_question(question_obj, all_questions):
    """Applies data augmentation methods to a question."""
    augmented_questions = []

    try:
        base_qid = question_obj['qid']
        question = question_obj['question']
        chunk = question_obj['chunk']
        parent_qid = base_qid
    except:
        return None

    if not question:
        return None

    # 方法1：問題換同義詞（擴充5次）
    tagone = "questionSynonymChange"
    # 生成方法特定的轉換
    prompt = questionSynonymChange(question)
    method_question = call_gpt(prompt)
    if method_question:
        augmented_questions.extend(expand_question(base_qid, parent_qid, tagone, method_question))

    # 方法3：複合問題 x2（擴充5次）
    tagone = "complexQuestionX2"
    # 生成方法特定的轉換（組合兩個問題）
    other_questions = [q for q in all_questions if q['qid'] != base_qid]
    import random
    other_question_obj = random.choice(other_questions)
    other_question = other_question_obj['question']
    prompt = complexQuestionX2(question, other_question)
    method_question = call_gpt(prompt)
    if method_question:
        augmented_questions.extend(expand_question(base_qid, parent_qid, tagone, method_question))

    # 方法4：複合問題 x3（擴充5次）
    tagone = "complexQuestionX3"
    # 生成方法特定的轉換（組合三個問題）
    other_questions = [q for q in all_questions if q['qid'] != base_qid]
    other_question_obj1 = random.choice(other_questions)
    other_question_obj2 = random.choice(other_questions)
    while other_question_obj2['qid'] == other_question_obj1['qid']:
        other_question_obj2 = random.choice(other_questions)
    other_question1 = other_question_obj1['question']
    other_question2 = other_question_obj2['question']
    prompt = complexQuestionX3(question, other_question1, other_question2)
    method_question = call_gpt(prompt)
    if method_question:
        augmented_questions.extend(expand_question(base_qid, parent_qid, tagone, method_question))

    # 以下為不使用 'func' 的方法
    # 方法2：問題隨知識style
    tagone = "questionWithKnowledgeStyle"
    tagtwo = ""
    prompt = questionWithKnowledgeStyle(question, chunk)
    knowledge_style_question = call_gpt(prompt)
    if knowledge_style_question:
        augmented_questions.append({
            "qid": f"{base_qid}_2",
            "parentqid": parent_qid,
            "tagone": tagone,
            "tagtwo": tagtwo,
            "question": knowledge_style_question
        })

    # 方法5：問題 + 關鍵字
    tagone = "questionWithKeyword"
    tagtwo = ""
    prompt = keyword(question)
    question_with_keyword = call_gpt(prompt)
    if question_with_keyword:
        question_with_keywordr = question + " " + question_with_keyword
        augmented_questions.append({
            "qid": f"{base_qid}_5",
            "parentqid": parent_qid,
            "tagone": tagone,
            "tagtwo": tagtwo,
            "question": question_with_keywordr
        })

    # 方法6：問題 + 同義詞
    tagone = "questionWithSynonym"
    tagtwo = ""
    prompt = questionWithSynonym(question)
    question_with_synonym = call_gpt(prompt)
    if question_with_synonym:
        question_with_synonym = question + " " + question_with_synonym
        augmented_questions.append({
            "qid": f"{base_qid}_6",
            "parentqid": parent_qid,
            "tagone": tagone,
            "tagtwo": tagtwo,
            "question": question_with_synonym
        })

    # 方法7：問題 + 關鍵字 + 同義詞
    tagone = "questionWithKeywordAndSynonym"
    tagtwo = ""
    if question_with_synonym:
        if question_with_keyword:
            question_with_keyword_synonym = question_with_synonym + " " + question_with_keyword
            augmented_questions.append({
                "qid": f"{base_qid}_7",
                "parentqid": parent_qid,
                "tagone": tagone,
                "tagtwo": tagtwo,
                "question": question_with_keyword_synonym
            })

    return augmented_questions

if __name__ == "__main__":
    with open('src/autogenq_1119/law_dataset(公務員相關法規).txt', 'r', encoding='utf-8') as f:
        text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=210,
        chunk_overlap=1,
    )
    chunks = text_splitter.split_text(text)

    questions = generate_questions(chunks)

    all_augmented_questions = []
    for question_obj in tqdm(questions, desc="Applying data augmentation"):
        augmented = augment_question(question_obj, questions)
        if augmented:
            all_augmented_questions.extend(augmented)

    output_data = []
    for item in all_augmented_questions:
        output_data.append({
            "qid": item['qid'],
            "parentqid": item['parentqid'],
            "tagone": item['tagone'],
            "tagtwo": item['tagtwo'],
            "question": item['question']
        })

    with open('src/autogenq_1119/output.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("Data augmentation complete. Output saved to output.json")
