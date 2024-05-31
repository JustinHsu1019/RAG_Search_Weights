from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import requests, json, io

from utils.weaviate_op import search_do
from utils.call_ai import call_aied
from utils.gpt_tem import GPT_Template

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type, Qs-PageCode, Cache-Control'

url_template = "http://127.0.0.1:5000/chat?mess={question}&alpha={alpha}"

@app.route("/")
def index():
    """Server 是否正常的確認頁面.
    """
    return "server is ready"

@app.route("/chat", methods=['POST', 'GET'])
def chat_bot():
    question = request.values.get("mess")
    alpha = request.values.get("alpha")

    if not question:
        response = "無內容"
    else:
        try:
            response_li = search_do(question, alp=alpha)
            response = call_aied(response_li, question)
        except Exception as e:
            print(f"get error: {e}")
            response = f"Error: {e}"

    return jsonify({"llm": response, "retriv": response_li})

def verify_retriv_response(retriv_response, answer):
    for i in range(len(retriv_response)):
        retriv_response[i] = retriv_response[i].replace('"','').replace('\n','').replace('\\n','').replace('\\','').replace(' ','')
    return "yes" if answer in retriv_response else "no"

def verify_llm_response(llm_response, answer):
    prompt = f'問題: {llm_response} 與 {answer} 是否意思相同？是的話請回傳 yes，不是的話請回傳 no，只有這兩種回應，不要回其他東西。請用 json 格式回傳，{{"回傳內容": "yes"}}'
    response = json.loads(GPT_Template(prompt))
    return "yes" if response["回傳內容"] == "yes" else "no"

@app.route('/llmautotest', methods=['POST'])
def process_excel():
    file = request.files['file']
    df = pd.read_excel(file)

    questions = df['問題'].tolist()
    answers = df['答案'].tolist()

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for alpha in [round(x * 0.1, 1) for x in range(10, 0, -1)]:
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

            result_df = pd.DataFrame({
                '問題': questions,
                '答案': answers,
                f'檢索結果_{alpha}': retriv_results,
                f'GPT_結果_{alpha}': llm_results,
                f'檢索驗證_{alpha}': retriv_validation,
                f'答案驗證_{alpha}': llm_validation
            })

            sheet_name = f'alpha {alpha}'
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)

    output.seek(0)
    return send_file(output, download_name='processed_results.xlsx', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)


""" JWT 驗證版 """
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from datetime import timedelta

# from utils.weaviate_op import search_do
# from utils.call_ai import call_aied
# import utils.config_log as config_log
# config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
# config.read(CONFIG_PATH)

# app = Flask(__name__)
# CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type, Qs-PageCode, Cache-Control'

# app.config['JWT_SECRET_KEY'] = config.get("Test_Acc", 'jwt_key')
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
# jwt_manager = JWTManager(app)

# @app.route("/")
# def index():
#     """Server health check."""
#     return "server is ready"

# @app.route("/login", methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     if username == config.get("Test_Acc", 'username') and password == config.get("Test_Acc", 'password'):
#         user_info = {"username": username}
#         access_token = create_access_token(identity=user_info)
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify({"message": "Invalid credentials"}), 401

# @app.route("/chat", methods=['POST'])
# @jwt_required()
# def chat_bot():
#     question = request.values.get("mess")
#     # alpha = request.values.get("alpha")
#     alpha = 0.5

#     if not question:
#         response = "無內容"
#     else:
#         try:
#             response_li = search_do(question, alp=alpha)
#             response = call_aied(response_li, question)
#         except Exception as e:
#             print(f"get error: {e}")
#             response = f"Error: {e}"

#     return jsonify({"llm": response, "retriv": response_li})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, threaded=True)
