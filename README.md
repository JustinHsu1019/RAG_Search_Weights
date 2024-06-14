# 探索 RAG 中關鍵字與向量搜尋結合的最佳權重配置
近年來，RAG（Retrieval Augmented Generation）作為新興的生成式 AI 技術備受關注。RAG 架構中的檢索器對文本的查詢方式直接影響著檢索的準確性，進而決定了系統的整體性能。本報告旨在探索在 RAG 中結合關鍵字匹配和向量語意搜尋的最佳權重配置。我們將通過以下步驟進行分析：
1. RAG 的檢索基於關鍵字匹配（基於 BM25F 方法）和向量語意搜尋（基於 Word2Vec + 餘弦相似度方法），將關鍵字匹配和向量語意搜尋結合，針對教育領域 (選課機器人) 窮舉出最佳權重配置
2. 利用 LLM 對測試資料進行自動測試和評分
3. 匯總不同權重配置（從 10:0 ~ 1:9）的測試結果
4. 將結果進行統計和視覺化，展示各種權重配置下的檢索準確性與系統性能
5. 分析不同權重配置對檢索準確性和系統性能的影響及造成此分布的原因

## 專題發表影片
[![](https://img.youtube.com/vi/OGzUFCVihws/0.jpg)](https://www.youtube.com/embed/OGzUFCVihws?si=3bWzFjl45HAsSeh6)

## 研究相關介紹

### RAG (Retrieval-Augmented Generation)
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/4.jpg)

### Prompt (提示詞) 比較
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/5.jpg)

### 研究動機
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/6.jpg)

### 提出問題
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/7.jpg)

### 參考文獻
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/8.jpg)

### 研究方法
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/9.jpg)

### 資料說明
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/10.jpg)

### 研究結果展示 (第一次試驗)
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/11.jpg)

### 研究結果展示 (第二次試驗)
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/12.jpg)

### 結論
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/13.jpg)
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/14.jpg)

### 未來展望
![](https://raw.githubusercontent.com/JustinHsu1019/RAG_Search_Weights/main/img/15.jpg)
