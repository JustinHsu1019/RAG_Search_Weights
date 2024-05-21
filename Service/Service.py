from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.weaviate_op import search_do
from utils.call_ai import call_aied

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type, Qs-PageCode, Cache-Control'

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

if __name__ == "__main__":
    app.run(threaded=True)
