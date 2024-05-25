# import os
# import uuid, time
# import weaviate
# from langchain.embeddings import OpenAIEmbeddings

# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import Service.utils.config_log as config_log
# config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
# config.read(CONFIG_PATH)

# Azure_Open_AI_VERSION = 'Open_AI'
# os.environ["OPENAI_API_TYPE"] = config.get(Azure_Open_AI_VERSION, 'api_type')
# os.environ["OPENAI_API_VERSION"] = config.get(Azure_Open_AI_VERSION, 'api_version')
# os.environ["OPENAI_API_BASE"] = config.get(Azure_Open_AI_VERSION, 'azure_endpoint')
# os.environ["OPENAI_API_KEY"] = config.get(Azure_Open_AI_VERSION, 'api_key')

# class WeaviateManager:
#     def __init__(self, classNm):
#         self.url = config.get('Weaviate', 'weaviate_url')
#         self.embeddings = OpenAIEmbeddings(chunk_size=1, model=config.get(Azure_Open_AI_VERSION, 'embedding_model_search'))
#         self.client = weaviate.Client(
#             url=config.get('Weaviate', 'weaviate_url'),
#             additional_headers={"X-Azure-Api-Key": f"{config.get('Weaviate', 'api_key')}"}
#         )
#         self.schema = self.client.schema
#         self.classNm = classNm
#         self.check_class_exist()
#         pass

#     def check_class_exist(self):
#         if self.client.schema.exists(self.classNm):
#             print(f'{self.classNm} is ready')
#             return True
#         schema = {
#             "class": self.classNm,
#             "properties": [
#                 {
#                     "name": "uuid",
#                     "dataType": ["text"]
#                 },
#                 {
#                     "name": "title",
#                     "dataType": ["text"]
#                 },
#                 {
#                     "name": "content",
#                     "dataType": ["text"]
#                 }
#             ],
#             "vectorizer": "text2vec-openai",
#             "moduleConfig": {
#                 "text2vec-openai": {
#                     "resourceName": config.get(Azure_Open_AI_VERSION, 'resourcename'),
#                     "deploymentId": config.get(Azure_Open_AI_VERSION, 'embedding_model_search')
#                 }
#             }
#         }
#         print(f'creating {self.classNm}...')
#         self.client.schema.create_class(schema)
#         print(f'{self.classNm} is ready')
#         return True

#     def insert_data(self, title_text, content_text):
#         data_object = {
#             "uuid": str(uuid.uuid4()),
#             "title": title_text,
#             "content": content_text
#         }
#         max_retries = 5
#         for attempt in range(max_retries):
#             try:
#                 self.client.data_object.create(data_object, self.classNm)
#                 break
#             except Exception as e:
#                 if "429" in str(e):
#                     print(f"Rate limit exceeded, retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
#                     time.sleep(5)
#                 else:
#                     raise
#         self.client.data_object.create(data_object, self.classNm)

# if __name__ == "__main__":
#     manager = WeaviateManager(config.get('Weaviate', 'classnm'))

#     with open("Data/OPT/class_data.txt", 'r', encoding='utf-8') as file:
#         content = file.read()

#     new_cp = content.split("justinhsu")
#     index = 0
#     for i in new_cp:
#         index += 1
#         manager.insert_data("標題", i)

#     print(new_cp[1])
#     print("\n\n" + index)

import os
import uuid
import time
import weaviate
from sentence_transformers import SentenceTransformer

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Service.utils.config_log as config_log
config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

wea_url = config.get('Weaviate', 'weaviate_url')
vdb = config.get('Weaviate', 'classnm')

class WeaviateManager:
    def __init__(self, classNm):
        self.url = wea_url
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = weaviate.Client(url=wea_url)
        self.classNm = classNm
        self.check_class_exist()

    def check_class_exist(self):
        if self.client.schema.exists(self.classNm):
            print(f'{self.classNm} is ready')
            return True
        schema = {
            "class": self.classNm,
            "properties": [
                {"name": "uuid", "dataType": ["text"]},
                {"name": "title", "dataType": ["text"]},
                {"name": "content", "dataType": ["text"]}
            ],
            "vectorizer": "text2vec-transformers"
        }
        print(f'creating {self.classNm}...')
        self.client.schema.create_class(schema)
        print(f'{self.classNm} is ready')
        return True

    def insert_data(self, title_text, content_text):
        data_object = {
            "uuid": str(uuid.uuid4()),
            "title": title_text,
            "content": content_text
        }
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.client.data_object.create(data_object, self.classNm)
                break
            except weaviate.exceptions.RequestError as e:
                if "429" in str(e):
                    print(f"Rate limit exceeded, retrying in 5 seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                else:
                    raise
        self.client.data_object.create(data_object, self.classNm)

if __name__ == "__main__":
    manager = WeaviateManager(vdb)

    with open("Data/OPT/class_data.txt", 'r', encoding='utf-8') as file:
        content = file.read()

    new_cp = content.split("justinhsu")
    for index, i in enumerate(new_cp, 1):
        manager.insert_data("標題", i)

    print(new_cp[1])
    print("\n\n" + str(index))
