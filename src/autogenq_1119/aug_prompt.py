def questionSynonymChange(question):
    return f"""請將以下問題中的關鍵字都替換為同義詞，保持語意不變，並輸出改變後的問題

原始問題：{question}

輸出格式：請直接輸出問題，不要輸出任何其他內容。
"""

def complexQuestionX2(question, other_question):
    return f"""請將以下兩個問題組合成一個語意較複雜的複合問題，並輸出整合後的問題

1. {question}
2. {other_question}

輸出格式：請直接輸出問題，不要輸出任何其他內容。
"""

def complexQuestionX3(question, other_question1, other_question2):
    return f"""請將以下三個問題組合成一個語意較複雜的複合問題，並輸出整合後的問題

1. {question}
2. {other_question1}
3. {other_question2}

輸出格式：請直接輸出問題，不要輸出任何其他內容。
"""

def questionWithKnowledgeStyle(question, chunk):
    return f"""請將以下原始問題改寫，根據下述"法律條文文章範例"使問題style表述為法律條文的文字風格，並輸出改變後的問題

法律條文文章範例：{chunk}

原始問題：{question}

輸出格式：請直接輸出問題，不要輸出任何其他內容。
"""

def questionWithSynonym(question):
    return f"""請將以下原始問題中的關鍵字都提取出，並全部替換為同義詞，並用空格分開輸出

原始問題：{question}

輸出格式：請直接輸出結果，不要輸出任何其他內容。
"""
