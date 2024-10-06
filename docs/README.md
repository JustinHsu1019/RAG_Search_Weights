# Benchmark Dataset

Dataset: [MediaTek-Research/TCEval-v2](https://huggingface.co/datasets/MediaTek-Research/TCEval-v2)

## 資料集選擇

**台達閱讀理解資料集**：
   - **前言**：使用聯發科整理的 TCEval-v2 資料集中的台達閱讀理解資料集 drcd，其中有不重複文章段落共 1000 段，以及對應的 3493 個問題。
   - **子集**：`drcd`（大規模中文閱讀理解數據集，3493條）
   - **欄位名稱**：```['id', 'paragraph', 'question', 'references']```
   - **特點**：涵蓋廣泛主題，文本組成多樣，適合測試在綜合性內容中的檢索效果。
   - **資料範例**：
   ```json
   {
      "id": "test-800",
      "paragraph": "登山車車名的由來 則是有一位來自Sunta Barbara的腳踏車狂熱份子Jame McCleam，建議Fisher將這類型的改良式腳踏車命名為登山車，於是登山車名稱的確立開始於此。在早期的登山車比賽中，他們所造的登山車包辦了所有比賽中的錦標。蓋瑞費雪的第一部登山車，及他本人都進入了美國登山車協會的名人堂，這對一個畢身從事登山車賽的愛好者來說，是一項最高的榮譽。有一段很長的時間，蓋瑞及湯姆合作生產登山車的行銷工作。 但是從他們倆人最後分手，蓋瑞轉向日本人訂購車身。那時日本人做的鋁合金的車身輕巧耐用，在八零年代，最好的登山車重量都在三十磅以下。有史以來第一次的登山車越野競賽名叫瑞派克。 是在一九七九年一個秋高氣爽的日子在美國北加州 一個叫泰馬派山的一條防火道上舉行的。什麼是防火道呢？在美國境內有許多的高山，有些有路，有些沒有路可以供人登山， 但是它一定會開闢一條可供救火車行駛的山道 以便森林火災發生的時候可以上山救火，這條山道往往非常簡陋，沒有柏油路面，只是就地取材，用碎石子鋪成，反正只要救火車能開便行了。在泰馬派山這條防火山道全長二千九百公尺，垂直高四百公尺，最小的坡14度最大的20度。當第一次比賽時，賽完全程的改良式老爺車到達終點時， 剎車部份的剎車油已在下坡猛剎時被用得精光，冒出陣陣白色的濃煙!為了紀念這一次比賽，從此泰馬派山的這條防火山道便被命名為瑞派克路，所以瑞派克競賽可說是現代登山車競賽的始祖。",
      "question": "對登山車賽的愛好者來說可以進去哪個組織的名人堂是一生中的榮耀?",
      "references": ["美國登山車協會"]
   }
   ```
   - **細節**：將`paragraph`作為存入 weaviate 的正確答案，`question`作為丟入 retrieval 的 query。只需將此 1000 篇`paragraph` 存入 weaviate (需用程式匹配重複)，並將`question`及`paragraph`存入一份 excel 檔案，之後對答案用。
   - **代辦事項**：完成所有工作後，利用 LLM 將此資料集分類，使最終能取得對應**不同領域**分別的評測結果。
   - **Embedding 模型選擇**：text-embedding-3-large
   - **繁體中文斷詞**：LLM 斷詞 or [CKIP Transformers](https://github.com/ckiplab/ckip-transformers)
   - **平均 Hit Rate (命中率)**：取 top_k 是 1，在撈出來最相似的 1 筆中，是否包含正確 context。有中就1分，沒中是0分
   - **平均 Mean Reciprocal Rank (MRR 平均倒數排名)**：(目前 top_k = 1 用不到) 在撈出來的幾筆中，正確的 context 排在第幾名?，若排第一得1分，排第三是 1/3 分 (取倒數)，沒中就是0分
   - **參考文獻**：[ihower: 使用繁體中文評測各家 Embedding 模型的檢索能力](https://ihower.tw/blog/archives/12167)

## 附錄：資料集介紹

```
Subset: drcd, Row Count: 3493
Subset: mt_bench_tw-coding, Row Count: 10
Subset: mt_bench_tw-extraction, Row Count: 10
Subset: mt_bench_tw-humanities, Row Count: 10
Subset: mt_bench_tw-math, Row Count: 10
Subset: mt_bench_tw-reasoning, Row Count: 10
Subset: mt_bench_tw-roleplay, Row Count: 10
Subset: mt_bench_tw-stem, Row Count: 10
Subset: mt_bench_tw-writing, Row Count: 10
Subset: penguin_table, Row Count: 144
Subset: tmmluplus-accounting, Row Count: 191
Subset: tmmluplus-administrative_law, Row Count: 420
Subset: tmmluplus-advance_chemistry, Row Count: 123
Subset: tmmluplus-agriculture, Row Count: 151
Subset: tmmluplus-anti_money_laundering, Row Count: 134
Subset: tmmluplus-auditing, Row Count: 550
Subset: tmmluplus-basic_medical_science, Row Count: 954
Subset: tmmluplus-business_management, Row Count: 139
Subset: tmmluplus-chinese_language_and_literature, Row Count: 199
Subset: tmmluplus-clinical_psychology, Row Count: 125
Subset: tmmluplus-computer_science, Row Count: 174
Subset: tmmluplus-culinary_skills, Row Count: 292
Subset: tmmluplus-dentistry, Row Count: 399
Subset: tmmluplus-economics, Row Count: 393
Subset: tmmluplus-education, Row Count: 124
Subset: tmmluplus-education_(profession_level), Row Count: 486
Subset: tmmluplus-educational_psychology, Row Count: 176
Subset: tmmluplus-engineering_math, Row Count: 103
Subset: tmmluplus-finance_banking, Row Count: 135
Subset: tmmluplus-financial_analysis, Row Count: 382
Subset: tmmluplus-fire_science, Row Count: 124
Subset: tmmluplus-general_principles_of_law, Row Count: 106
Subset: tmmluplus-geography_of_taiwan, Row Count: 768
Subset: tmmluplus-human_behavior, Row Count: 309
Subset: tmmluplus-insurance_studies, Row Count: 760
Subset: tmmluplus-introduction_to_law, Row Count: 237
Subset: tmmluplus-jce_humanities, Row Count: 90
Subset: tmmluplus-junior_chemistry, Row Count: 209
Subset: tmmluplus-junior_chinese_exam, Row Count: 175
Subset: tmmluplus-junior_math_exam, Row Count: 175
Subset: tmmluplus-junior_science_exam, Row Count: 213
Subset: tmmluplus-junior_social_studies, Row Count: 126
Subset: tmmluplus-logic_reasoning, Row Count: 139
Subset: tmmluplus-macroeconomics, Row Count: 411
Subset: tmmluplus-management_accounting, Row Count: 215
Subset: tmmluplus-marketing_management, Row Count: 93
Subset: tmmluplus-mechanical, Row Count: 118
Subset: tmmluplus-music, Row Count: 278
Subset: tmmluplus-national_protection, Row Count: 211
Subset: tmmluplus-nautical_science, Row Count: 551
Subset: tmmluplus-occupational_therapy_for_psychological_disorders, Row Count: 543
Subset: tmmluplus-official_document_management, Row Count: 222
Subset: tmmluplus-optometry, Row Count: 920
Subset: tmmluplus-organic_chemistry, Row Count: 109
Subset: tmmluplus-pharmacology, Row Count: 577
Subset: tmmluplus-pharmacy, Row Count: 391
Subset: tmmluplus-physical_education, Row Count: 179
Subset: tmmluplus-physics, Row Count: 97
Subset: tmmluplus-politic_science, Row Count: 995
Subset: tmmluplus-real_estate, Row Count: 92
Subset: tmmluplus-secondary_physics, Row Count: 112
Subset: tmmluplus-statistics_and_machine_learning, Row Count: 224
Subset: tmmluplus-taiwanese_hokkien, Row Count: 129
Subset: tmmluplus-taxation, Row Count: 375
Subset: tmmluplus-technical, Row Count: 402
Subset: tmmluplus-three_principles_of_people, Row Count: 139
Subset: tmmluplus-trade, Row Count: 502
Subset: tmmluplus-traditional_chinese_medicine_clinical_medicine, Row Count: 278
Subset: tmmluplus-trust_practice, Row Count: 401
Subset: tmmluplus-ttqav2, Row Count: 113
Subset: tmmluplus-tve_chinese_language, Row Count: 483
Subset: tmmluplus-tve_design, Row Count: 480
Subset: tmmluplus-tve_mathematics, Row Count: 150
Subset: tmmluplus-tve_natural_sciences, Row Count: 424
Subset: tmmluplus-veterinary_pathology, Row Count: 283
Subset: tmmluplus-veterinary_pharmacology, Row Count: 540
```
