import os
import time
import weaviate
import sys
from datasets import load_dataset

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

wea_url = config.get("Weaviate", "weaviate_url")
openai_api_key = config.get("OpenAI", "api_key")
PROPERTIES = ["uuid", "content"]


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
    dataset_name = "MediaTek-Research/TCEval-v2"
    subset = "drcd"
    ds = load_dataset(dataset_name, subset)

    manager = WeaviateManager(config.get("Weaviate", "classnm"))

    latest_p = None

    for entry in ds["test"]:
        id = entry["id"]
        cont = entry["paragraph"]

        if cont != latest_p:
            manager.insert_data(id, cont)
            latest_p = cont
        else:
            print(f"Skipping duplicate paragraph for id={id}")

    print("資料已成功存入 Weaviate!")


if __name__ == "__main__2":
    manager = WeaviateManager(config.get("Weaviate", "classnm"))

    with open("src/backup/data/【課程評價】_110112.txt", "r", encoding="utf-8") as file:
        content = file.read()

    new_cp = content.split("JustinHsu")
    # print(new_cp[0])

    for index, i in enumerate(new_cp, 1):
        manager.insert_data(str(index), i)

    print(new_cp[1])
    print("\n\n" + str(index))
