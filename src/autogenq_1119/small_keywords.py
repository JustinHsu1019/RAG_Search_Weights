def small_key(q, keys):
    return f"""
我的核心衷旨是要問出 [原始問題] 的問題，也就是利用 Keywords 的形式來 Google Search，一樣要能得到用 [原始問題] 來問的答案，
但是 Google Search 講求的是用 Keywords 的形式搜尋，所以我做了 [原始 Keywords]
但我現在還是覺得 [原始 Keywords] 太多了，所以我要你幫我縮減成 [縮減後 Keywords]
請幫我維持問題原意，但精簡並刪除不必要的關鍵字，最後用空格來分割關鍵字輸出

[原始問題]: {q}
[原始 Keywords]: {keys}

輸出格式：請直接輸出結果，不要輸出任何其他內容。
"""
