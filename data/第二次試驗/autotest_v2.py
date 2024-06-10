import weaviate
from langchain.embeddings import AzureOpenAIEmbeddings
import sys, os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import backend.utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

Azure_Open_AI_VERSION = 'Open_AI'
os.environ["OPENAI_API_TYPE"] = config.get(Azure_Open_AI_VERSION, 'api_type')
os.environ["OPENAI_API_VERSION"] = config.get(Azure_Open_AI_VERSION, 'api_version')
os.environ["OPENAI_API_BASE"] = config.get(Azure_Open_AI_VERSION, 'azure_endpoint')
os.environ["OPENAI_API_KEY"] = config.get(Azure_Open_AI_VERSION, 'api_key')

wea_url = config.get('Weaviate', 'weaviate_url')
api_key = config.get(Azure_Open_AI_VERSION, 'api_key')
vdb = config.get('Weaviate', 'classnm')

class WeaviateSemanticSearch:
    def __init__(self, classNm):
        self.url = wea_url
        self.embeddings = AzureOpenAIEmbeddings(chunk_size=1, model="text-embedding-ada-002", api_key=api_key)
        self.client = weaviate.Client(
            url=wea_url,
            additional_headers={"X-Azure-Api-Key": api_key}
        )
        self.classNm = classNm

    def vector_search(self, query_text, num_results=2622):
        query_vector = self.embeddings.embed_query(query_text)
        vector_str = ",".join(map(str, query_vector))
        
        gql_query = f"""
        {{
            Get {{
                {self.classNm}(hybrid: {{query: "{query_text}", vector: [{vector_str}], alpha: 1 }}, limit: {num_results}) {{
                    content
                    _additional {{
                        distance
                        score
                    }}
                }}
            }}
        }}
        """
        search_results = self.client.query.raw(gql_query)
        results = search_results['data']['Get'][self.classNm]
        return results

    def keyword_search(self, query_text, num_results=2622):
        gql_query = f"""
        {{
            Get {{
                {self.classNm}(hybrid: {{query: "{query_text}", vector: [], alpha: 0 }}, limit: {num_results}) {{
                    content
                    _additional {{
                        score
                    }}
                }}
            }}
        }}
        """
        search_results = self.client.query.raw(gql_query)
        results = search_results['data']['Get'][self.classNm]
        return results

    def hybrid_search(self, query, keywords, alpha, num_results=3):
        vector_results = self.vector_search(query, 2622)
        keyword_results = self.keyword_search(keywords, 2622)
        
        vector_scores = {result['content']: float(result['_additional']['score']) for result in vector_results}
        keyword_scores = {result['content']: float(result['_additional']['score']) for result in keyword_results}

        all_contents = list(set(vector_scores.keys()).union(keyword_scores.keys()))
        combined_scores = {}
        
        for content in all_contents:
            vec_score = vector_scores.get(content, 0)
            key_score = keyword_scores.get(content, 0)
            combined_score = alpha * vec_score + (1 - alpha) * key_score
            combined_scores[content] = combined_score

        sorted_combined_scores = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        top_results = [item[0] for item in sorted_combined_scores[:num_results]]
        return top_results

def process_excel(file_path):
    df = pd.read_excel(file_path)
    questions = df['問題'].tolist()
    answers = df['答案'].tolist()
    keywords = df['關鍵字'].tolist()

    searcher = WeaviateSemanticSearch(vdb)
    results = []

    for question, answer, keyword in zip(questions, answers, keywords):
        for alpha in [round(x * 0.1, 1) for x in range(10, 0, -1)]:
            result = searcher.hybrid_search(question, keyword, alpha, num_results=3)
            results.append({
                '問題': question,
                '答案': answer,
                '關鍵字': keyword,
                f'檢索結果_{alpha}': result
            })

    result_df = pd.DataFrame(results)
    result_df.to_excel('data/第二次試驗/【測試結果】_60題.xlsx', index=False)
    print("混合搜索完成並已保存結果。")

process_excel('data/第二次試驗/【測試資料】_60題.xlsx')
