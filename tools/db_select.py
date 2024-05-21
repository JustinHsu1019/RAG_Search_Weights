import os
import weaviate

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Service.utils.config_log as config_log
config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

Azure_Open_AI_VERSION = 'Open_AI'
os.environ["OPENAI_API_TYPE"] = config.get(Azure_Open_AI_VERSION, 'api_type')
os.environ["OPENAI_API_VERSION"] = config.get(Azure_Open_AI_VERSION, 'api_version')
os.environ["OPENAI_API_BASE"] = config.get(Azure_Open_AI_VERSION, 'azure_endpoint')
os.environ["OPENAI_API_KEY"] = config.get(Azure_Open_AI_VERSION, 'api_key')

PROPERITIES = ["uuid", "title", "content"]
classNm = config.get('Weaviate', 'classnm')

# 統計筆數
if __name__ == "__main__1":
    client = weaviate.Client(url=config.get('Weaviate', 'weaviate_url'),
                             additional_headers={"X-Azure-Api-Key": f"{config.get(Azure_Open_AI_VERSION, 'api_key')}"})
    print(client.query.aggregate(classNm).with_meta_count().do())

# 顯示所有資料
if __name__ == "__main__2":
    client = weaviate.Client(url=config.get('Weaviate', 'weaviate_url'),
                             additional_headers={"X-Azure-Api-Key": f"{config.get(Azure_Open_AI_VERSION, 'api_key')}"})
    client.schema.exists(classNm)

    result = client.query.get(class_name=classNm, properties=PROPERITIES).with_limit(3).do()

    print(str(result))

# 刪除此向量庫
if __name__ == "__main__3":
    client = weaviate.Client(url=config.get('Weaviate', 'weaviate_url'),
                             additional_headers={"X-Azure-Api-Key": f"{config.get(Azure_Open_AI_VERSION, 'api_key')}"})
    client.schema.delete_class(classNm)
