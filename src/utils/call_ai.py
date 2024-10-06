import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.gpt_tem import GPT_Template


def call_aied(question):
    prompt = f"""
[題目]：{question}

請幫我提取 [題目] 中你認為的關鍵字

用空格隔開輸出

輸出範例：
關鍵字1 關鍵字2 關鍵字3

Start directly with the first keyword, avoid any unnecessary introduction.
"""
    try:
        res = GPT_Template(prompt)
    except:
        res = question

    return res
