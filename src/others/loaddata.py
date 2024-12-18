import pandas as pd
from datasets import load_dataset


def load_dataset_from_hf():
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


def insert_data(idd, cont, data_list):
    data_list.append({"id": idd, "paragraph": cont})


def create_id_cont_mapping():
    dataset_name = "MediaTek-Research/TCEval-v2"
    subset = "drcd"
    ds = load_dataset(dataset_name, subset)

    data_list = []
    latest_p = None

    for entry in ds["test"]:
        cont = entry["paragraph"]

        if cont != latest_p:
            idd = entry["id"]
            insert_data(idd, cont, data_list)
            latest_p = cont

    df = pd.DataFrame(data_list)
    df.to_excel("result/test_1006/context_mapping.xlsx", index=False)

    print("成功!")


if __name__ == "__main__":
    # load_dataset_from_hf()
    create_id_cont_mapping()
