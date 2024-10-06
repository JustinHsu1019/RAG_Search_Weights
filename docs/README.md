# Benchmark Dataset

Dataset: [MediaTek-Research/TCEval-v2](https://huggingface.co/datasets/MediaTek-Research/TCEval-v2)

## 資料集選擇

1. **法律類**：
   - **子集**：`tmmluplus-administrative_law`（行政法，420條）
   - **取用方式**：取前200條資料
   - **特點**：題目包含複雜的法律術語和長句結構，有助於測試關鍵字匹配在專業術語中的效果。

2. **數學與物理類**：
   - **子集**：合併`tmmluplus-junior_math_exam`（國中數學考試，175條）、`tmmluplus-engineering_math`（工程數學，103條）、`tmmluplus-physics`（物理，97條）、`tmmluplus-secondary_physics`（高中物理，112條）
   - **取用方式**：合計約487條，隨機選取200條
   - **特點**：題目包含公式、符號和較短的問題描述，適合測試向量搜索在數理符號上的表現。

3. **醫學類**：
   - **子集**：`tmmluplus-basic_medical_science`（基礎醫學科學，954條）
   - **取用方式**：取前200條資料
   - **特點**：包含大量醫學專業術語和長句，測試在技術性強的文本中的檢索效果。

4. **計算機科學類**：
   - **子集**：合併`tmmluplus-computer_science`（計算機科學，174條）、`mt_bench_tw-coding`（編程，10條）、`tmmluplus-statistics_and_machine_learning`（統計與機器學習，224條）
   - **取用方式**：合計約408條，隨機選取200條
   - **特點**：可能包含代碼片段、算法描述，適合測試關鍵字與向量搜索在技術文本中的平衡。

5. **語言與文學類**：
   - **子集**：`tmmluplus-tve_chinese_language`（技專中文語言，483條）
   - **取用方式**：取前200條資料
   - **特點**：題目可能有較長的文本和文學性表達，適合測試在長語句和複雜語法中的檢索效果。

6. **財經與經濟類**：
   - **子集**：`tmmluplus-macroeconomics`（宏觀經濟學，411條）
   - **取用方式**：取前200條資料
   - **特點**：包含金融術語和專業知識，適合測試在專業領域中的檢索表現。

7. **社會科學與心理學類**：
   - **子集**：合併`tmmluplus-human_behavior`（人類行為學，309條）、`tmmluplus-educational_psychology`（教育心理學，176條）
   - **取用方式**：合計約485條，隨機選取200條
   - **特點**：涉及心理學、社會學術語，測試在抽象概念和專業詞彙中的檢索效果。

8. **藝術與音樂類**：
   - **子集**：`tmmluplus-music`（音樂，278條）
   - **取用方式**：取前200條資料
   - **特點**：題目可能包含樂譜、音樂術語，適合測試在藝術類文本中的檢索能力。

9. **綜合知識與閱讀理解類**：
   - **子集**：`drcd`（大規模中文閱讀理解數據集，3493條）
   - **取用方式**：取前200條資料
   - **特點**：涵蓋廣泛主題，文本組成多樣，適合測試在綜合性內容中的檢索效果。

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
