# 05/24 會議記錄

## 分工討論結果：
1. **[由許新翎負責]** RAG + LLM 自動測試程式設計 **[已完成]** / 報告統整+上台報告 **[已完成]**
2. **[由黃威昊負責]** QA Pair 製作 x30 題 (利用資料庫的課程製作，需有 15 題為句子形式，15 題為關鍵字形式，正確答案只會是完整的一堂課，盡量找可以對標到只有一個答案的) --> 利用資料庫上半課程做 **[已完成]**
3. **[由張元軍負責]** QA Pair 製作 x30 題 (利用資料庫的課程製作，需有 15 題為句子形式，15 題為關鍵字形式，正確答案只會是完整的一堂課，盡量找可以對標到只有一個答案的) --> 利用資料庫下半課程做 **[已完成]**
4. **[由黃中璟負責]** 資料處理 (檢索準確性 (%) / 答案準確性 (%) / 檢索準確性（標準化）/ 答案準確性（標準化）/ 綜合得分 / 根據綜合得分進行排序) --> 標準化分數 = (原始分數-最小值) / (最大值-最小值) --> 綜合得分 = 0.5×檢索準確性（標準化）+ 0.5×答案準確性（標準化） **[已完成]**
5. **[由李逸誠負責]** 資料可視化與圖表 (檢索準確性柱狀圖 / 答案準確性柱狀圖 / 混合圖表（檢索準確性和答案準確性對比）/ 趨勢圖 (展示不同權重配置下的準確性變化趨勢) / 綜合排序圖表) **[已完成]** + 製作 10 題驗證資料 **[已完成]**
6. **[由駱辰瑞負責]** 報告製作 (負責從封面到 RAG + LLM 介紹 / 主題介紹 / 做法介紹) --> 我會給相關資料，可以先開始做 **[已完成]**
7. **[由王宏毅負責]** 報告製作 (負責從資料處理結果開始 / 可視化+圖表展現 / 結論) --> 要跟資料處理兩人對接 **[已完成]**

## 時程表：
- **05/29(三)前**：黃威昊與張元軍將 QA Pair 共 60 題交於許新翎
- **05/30(四)前**：許新翎把 60 題放入 RAG + LLM 自動測試跑完並將結果 excel 交於黃中璟
- **06/03(一)前**：駱辰瑞完成報告製作前半段(各種介紹)，並交於許新翎
- **06/03(一)前**：黃中璟將資料處理完成，並將結果交於李逸誠與王宏毅
- **06/07(五)前**：李逸誠完成資料可視化與圖表並將結果交於王宏毅
- **06/10(一)前**：王宏毅利用黃中璟和李逸誠的資料結果完成報告後半段實驗結果/結論撰寫，並交於許新翎統整報告
- **06/14(五)**：許新翎在課堂上進行線上報告

## 現有程式碼：
- **RAG + LLM 自動測試-程式碼儲存庫**：[https://github.com/JustinHsu1019/RAG_Search_Weights](https://github.com/JustinHsu1019/RAG_Search_Weights)
- **課程資料 (請製作 QA Pair 的負責人參考此資料製作)**：[https://github.com/JustinHsu1019/RAG_Search_Weights/blob/main/data/class_data.txt](https://github.com/JustinHsu1019/RAG_Search_Weights/blob/main/data/class_data.txt)
- **QA Pair 製作結果 Excel 格式參考**：[https://github.com/JustinHsu1019/RAG_Search_Weights/blob/main/data/test/test_data.xlsx](https://github.com/JustinHsu1019/RAG_Search_Weights/blob/main/data/test/test_data.xlsx)
- **資料可視化與圖表的範例程式**：[https://colab.research.google.com/drive/1xxJYxCp3WO7PlU8oqknemf20dR3ee9J3?usp=sharing](https://colab.research.google.com/drive/1xxJYxCp3WO7PlU8oqknemf20dR3ee9J3?usp=sharing)
