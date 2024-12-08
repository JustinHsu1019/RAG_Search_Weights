def gene_q(chunk):
    return f"""
請為下列文章生成一題問題，並將問題的答案限制在文章中能回答的範圍內

文章：{chunk}

輸出格式：請直接輸出問題，不要輸出任何其他內容。
"""

def change_str(method_question):
    return f"""請在不改變語意的前提下，改變以下原始問題的句型 (e.g. 調換主詞和動詞位置)，並輸出改變後的問題

原始問題：{method_question}

輸出格式：請直接輸出問題，不要輸出任何其他內容。
"""

def condensed(method_question):
    return f"""請使用最精簡的文字來濃縮以下原始問題，並輸出濃縮後的問題

原始問題：{method_question}

輸出格式：請直接輸出問題，不要輸出任何其他內容。
"""

def keyword(method_question):
    return f"""請提取出以下原始問題的所有關鍵字，並用空格分開輸出

原始問題：{method_question}

輸出格式：請直接輸出結果，不要輸出任何其他內容。
"""
