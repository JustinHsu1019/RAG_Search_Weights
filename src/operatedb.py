import os
import time
import json
import weaviate
import sys
import warnings
from contextlib import redirect_stdout, redirect_stderr
from datasets import load_dataset

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.config_log as config_log
from utils.ckip import ws_driver, pos_driver, clean

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

wea_url = config.get("Weaviate", "weaviate_url")
openai_api_key = config.get("OpenAI", "api_key")
PROPERTIES = ["uuid", "content"]

# 忽略所有的 DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


def silent_call_ckip_v2(question):
    # 保存當前的 sys.stdout 和 sys.stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    try:
        # 使用 with 確保 stdout 和 stderr 正確地關閉，靜默所有輸出
        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull), redirect_stderr(fnull):
                ws = ws_driver([question])
                pos = pos_driver(ws)
    finally:
        # 恢復 sys.stdout 和 sys.stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
    return ws, pos


class WeaviateManager:
    def __init__(self, classNm):
        self.url = wea_url
        self.client = weaviate.Client(
            url=wea_url, additional_headers={"X-OpenAI-Api-Key": openai_api_key}
        )
        self.classNm = classNm
        self.check_class_exist()

    def aggregate_count(self):
        return self.client.query.aggregate(self.classNm).with_meta_count().do()

    def get_all_data(self, limit=100000):
        if self.client.schema.exists(self.classNm):
            result = (
                self.client.query.get(class_name=self.classNm, properties=PROPERTIES)
                .with_limit(limit)
                .do()
            )
            return result
        else:
            raise Exception(f"Class {self.classNm} does not exist.")

    def delete_class(self):
        self.client.schema.delete_class(self.classNm)

    def delete_data_by_custom_uuid(self, custom_uuid):
        """
        根據自定義的 uuid 欄位來過濾並刪除資料
        """
        try:
            gql_query = f"""
            {{
                Get {{
                    {self.classNm}(where: {{
                        path: ["uuid"],
                        operator: Equal,
                        valueString: "{custom_uuid}"
                    }}) {{
                        _additional {{
                            id
                        }}
                    }}
                }}
            }}
            """
            search_results = self.client.query.raw(gql_query)
            results = search_results["data"]["Get"][self.classNm]
            if results:
                for result in results:
                    obj_id = result["_additional"]["id"]
                    self.client.data_object.delete(obj_id)
                    print(f"Data with custom uuid {custom_uuid} deleted successfully.")
            else:
                print(f"No data found with custom uuid {custom_uuid}.")
        except weaviate.exceptions.RequestError as e:
            print(f"Error deleting data with custom uuid {custom_uuid}: {str(e)}")

    def check_class_exist(self):
        if self.client.schema.exists(self.classNm):
            print(f"{self.classNm} is ready")
            return True
        schema = {
            "class": self.classNm,
            "properties": [
                {"name": "uuid", "dataType": ["text"]},
                {"name": "content", "dataType": ["text"]},
            ],
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "text-embedding-3-large",
                    "dimensions": 3072,
                    "type": "text",
                }
            },
        }
        print(f"creating {self.classNm}...")
        self.client.schema.create_class(schema)
        print(f"{self.classNm} is ready")
        return True

    def insert_data(self, uuid, content_text):
        data_object = {"uuid": uuid, "content": content_text}
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.client.data_object.create(data_object, self.classNm)
                break
            except weaviate.exceptions.RequestError as e:
                if "429" in str(e):
                    print(
                        f"Rate limit exceeded, retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(5)
                else:
                    raise


if __name__ == "__main__1":
    """
    Vector Class
    """
    dataset_name = "MediaTek-Research/TCEval-v2"
    subset = "drcd"
    ds = load_dataset(dataset_name, subset)

    manager = WeaviateManager(config.get("Weaviate", "classnm"))

    latest_p = None

    for entry in ds["test"]:
        cont = entry["paragraph"]

        if cont != latest_p:
            idd = entry["id"]
            manager.insert_data(idd, cont)
            latest_p = cont

    print("資料已成功存入 Weaviate!")


if __name__ == "__main__2":
    """
    CKIP Keyword Class
    """
    dataset_name = "MediaTek-Research/TCEval-v2"
    subset = "drcd"
    ds = load_dataset(dataset_name, subset)

    manager = WeaviateManager(config.get("Weaviate", "keyclassnm"))

    latest_p = None

    for entry in ds["test"]:
        cont = entry["paragraph"]

        if cont != latest_p:
            ws, pos = silent_call_ckip_v2(cont)
            cont_keyword = clean(ws[0], pos[0])
            idd = entry["id"]
            manager.insert_data(idd, cont_keyword)
            latest_p = cont

    print("資料已成功存入 Key Weaviate!")


if __name__ == "__main__3":
    """
    Old Courses Class
    """
    manager = WeaviateManager(config.get("Weaviate", "classnm"))

    with open("src/backup/data/【課程評價】_110112.txt", "r", encoding="utf-8") as file:
        content = file.read()

    new_cp = content.split("JustinHsu")
    # print(new_cp[0])

    for index, i in enumerate(new_cp, 1):
        manager.insert_data(str(index), i)

    print(new_cp[1])
    print("\n\n" + str(index))


if __name__ == "__main__4":
    """
    測試「關鍵字」效果是否屬實
    """
    manager = WeaviateManager(config.get("Weaviate", "classnm"))

    manager.delete_data_by_custom_uuid("test-78")

    manager.insert_data(
        "test-79-1",
        """
由於缺乏有效的管理和協調，動物的學名命名非常混亂，同名異物、同物異名等現象層出不窮，最初由林奈制定的，簡單的分類和命名規則已經不符使用了，需要編制更完善和更嚴謹的命名規則。在這樣的背景下，19世紀下半葉在世界範圍內出現了許多各國自行制定的命名規則，其中比較有名的有：英國的史崔克蘭規則；美國則是由著名動物學家多爾，他發明了重要的命名法則，用他自己的名字作為這個規則的命名，同時也是多爾所屬的這個國家的鳥類學會，訂出了關於鳥類命名法則；法國動物學會規則；德意志動物學會規則；國際地質學會議關於動物化石命名的杜維爾規則。這些命名法規大多結構嚴謹，內容完善，但是相互獨立使得他們不能有效解決國際動物學界面臨的學名混亂問題。直到19世紀晚期國際動物學界普遍認同需要有一部統一的世界性動物學名命名規則。
""",
    )
    manager.insert_data(
        "test-79-2",
        """
1958年，在倫敦召開的第十五屆國際動物學會議通過了此前由國際動物命名法委員會主席布拉德利提交的法規草案。至此，世界性的動物命名規則完成了「法國規則－國際動物命名規則－國際動物命名規約」的轉變，以法規的形式穩定下來。此後，國際動物命名規則經歷了四次修訂，最近的一次修訂的版本是在1997年經過國際動物命名法委員會投票通過的。國際動物命名規約最初的執行解釋和修訂機構是國際動物學會議下設的國際動物命名法委員會，1972年在摩納哥召開的第十七屆國際動物學大會決定將原本定期召開的大會改為不定期召開，為了保持國際動物命名規約的延續性會議決定將其對國際動物命名規約的責任和義務轉移給國際生物學聯合會，現在國際生物科學聯合會下設的動物命名法委員會具體負責法規的解釋與修訂。
19世紀下半葉在世界範圍內出現了許多各國自行制定的命名規則，其中比較有名的有：英國的史崔克蘭規則；美國的多爾規則；法國動物學會規則；德意志動物學會規則；國際地質學會議關於動物化石命名的杜維爾規則；多爾出生的這個國家，有個鳥類學家協會，也出了一套關於鳥類命名的鳥類學家協會規則。
""",
    )
    manager.insert_data(
        "test-79-3",
        """
多爾、美國多爾、規、則、規則、美國、鳥類學家協會、鳥類學家協會規則、鳥類、多、協會、美、國
多爾鳥類學家協會、多爾鳥類、美國多爾鳥類學家、美國協會、多爾鳥、多爾協會
這是一個協會，這個協會在美國
這是一個專家，這個專家在美國
""",
    )


# ============= 12/10 新法規資料 =============

if __name__ == "__main__5":
    """
    Vector Class
    """
    json_path = "data/chunk.json"

    # 讀取新的 JSON 資料
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 初始化 Weaviate Manager
    manager = WeaviateManager(config.get("Weaviate", "classnm"))

    latest_p = None

    for entry in data:
        cont = entry["chunk"]
        if cont != latest_p:
            idd = entry["qid"]
            manager.insert_data(idd, cont)
            latest_p = cont

    print("資料已成功存入 Weaviate!")


if __name__ == "__main__6":
    """
    CKIP Keyword Class
    """
    json_path = "data/chunk.json"

    # 讀取新的 JSON 資料
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 初始化 Weaviate Manager
    manager = WeaviateManager(config.get("Weaviate", "keyclassnm"))

    latest_p = None

    for entry in data:
        cont = entry["chunk"]
        if cont != latest_p:
            ws, pos = silent_call_ckip_v2(cont)
            cont_keyword = clean(ws[0], pos[0])
            idd = entry["qid"]
            manager.insert_data(idd, cont_keyword)
            latest_p = cont

    print("資料已成功存入 Key Weaviate!")
