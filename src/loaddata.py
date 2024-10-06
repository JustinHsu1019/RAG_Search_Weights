import pandas as pd
from datasets import load_dataset

dataset_name = "MediaTek-Research/TCEval-v2"
subset = "drcd"

ds = load_dataset(dataset_name, subset)

data = {
    "id": ds["test"]["id"],
    "問題": ds["test"]["question"],
    "答案": ds["test"]["paragraph"],
}

df = pd.DataFrame(data)

output_file = "result/test_1006/testdata_3493.xlsx"
df.to_excel(output_file, index=False)

print(f"資料已儲存為 {output_file}")
