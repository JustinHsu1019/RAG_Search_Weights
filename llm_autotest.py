import pandas as pd
import requests
import json
from Service.utils.gpt_tem import GPT_Template

excel_path = 'data/test/test_data.xlsx'
df = pd.read_excel(excel_path)

questions = df['問題'].tolist()
answers = df['答案'].tolist()

def verify_retriv_response(retriv_response, answer):
    for i in range(len(retriv_response)):
        retriv_response[i] = retriv_response[i].replace('"','').replace('\n','').replace('\\n','').replace('\\','').replace(' ','')
    return "yes" if answer in retriv_response else "no"

def verify_llm_response(llm_response, answer):
    prompt = f'問題: {llm_response} 與 {answer} 是否意思相同？是的話請回傳 yes，不是的話請回傳 no，只有這兩種回應，不要回其他東西。請用 json 格式回傳，{{"回傳內容": "yes"}}'
    response = json.loads(GPT_Template(prompt))
    return "yes" if response["回傳內容"] == "yes" else "no"

url_template = "http://127.0.0.1:5000/chat?mess={question}&alpha={alpha}"

for alpha in [round(x * 0.1, 1) for x in range(1, 0, -1)]:
    retriv_validation = []
    llm_validation = []
    retriv_results = []
    llm_results = []

    for question, answer in zip(questions, answers):
        url = url_template.format(question=question, alpha=alpha)
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            retriv_results.append(result["retriv"])
            llm_results.append(result["llm"])
            retriv_validation.append(verify_retriv_response(result["retriv"], answer))
            llm_validation.append(verify_llm_response(result["llm"], answer))
        else:
            retriv_results.append("Failed to get response")
            llm_results.append("Failed to get response")
            retriv_validation.append("no")
            llm_validation.append("no")
            print(f"Failed to get response for question: {question} with alpha: {alpha}")

    df[f'檢索結果_{alpha}'] = retriv_results
    df[f'GPT_結果_{alpha}'] = llm_results
    df[f'檢索驗證_{alpha}'] = retriv_validation
    df[f'答案驗證_{alpha}'] = llm_validation

new_excel_path = 'data/test/test_result.xlsx'
df.to_excel(new_excel_path, index=False)
print(f"Saved results to {new_excel_path}")
