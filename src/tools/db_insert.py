import os
import time
import weaviate
import sys
from datasets import load_dataset

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import Service.utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

wea_url = config.get("Weaviate", "weaviate_url")
openai_api_key = config.get("OpenAI", "api_key")


class WeaviateManager:
    def __init__(self, classNm):
        self.url = wea_url
        self.client = weaviate.Client(
            url=wea_url, additional_headers={"X-OpenAI-Api-Key": openai_api_key}
        )
        self.classNm = classNm
        self.check_class_exist()

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


if __name__ == "__main__":
    dataset_name = "MediaTek-Research/TCEval-v2"
    subset = 'drcd'
    ds = load_dataset(dataset_name, subset)

    manager = WeaviateManager(config.get("Weaviate", "classnm"))

    for entry in ds['test']:
        id = entry['id']
        cont = entry['paragraph']
        manager.insert_data(id, cont)

    print("資料已成功存入 Weaviate!")
