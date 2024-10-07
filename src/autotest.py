import weaviate
from langchain.embeddings import OpenAIEmbeddings
import sys, os
import pandas as pd
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger

from utils.call_ai import call_aied

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import src.utils.config_log as config_log

config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

wea_url = config.get("Weaviate", "weaviate_url")
PROPERTIES = ["uuid", "content"]

os.environ["OPENAI_API_KEY"] = config.get("OpenAI", "api_key")


ws_driver = CkipWordSegmenter(model="albert-base")
pos_driver = CkipPosTagger(model="albert-base")


def clean(sentence_ws, sentence_pos):
    short_sentence = []
    stop_pos = set(["Nep", "Nh", "Nb"])
    for word_ws, word_pos in zip(sentence_ws, sentence_pos):
        is_N_or_V = word_pos.startswith("V") or word_pos.startswith("N")
        is_not_stop_pos = word_pos not in stop_pos
        is_not_one_charactor = not (len(word_ws) == 1)
        if is_N_or_V and is_not_stop_pos and is_not_one_charactor:
            short_sentence.append(f"{word_ws}")
    return " ".join(short_sentence)


class WeaviateSemanticSearch:
    def __init__(self, classNm):
        self.url = wea_url
        self.embeddings = OpenAIEmbeddings(chunk_size=1, model="text-embedding-3-large")
        self.client = weaviate.Client(url=wea_url)
        self.classNm = classNm

    def vector_search(self, query_text, num_results=1000):
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
        results = search_results["data"]["Get"][self.classNm]
        return results

    def keyword_search(self, query_text, num_results=1000):
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
        results = search_results["data"]["Get"][self.classNm]
        return results

    def hybrid_search(self, vector_results, keyword_results, alpha, num_results=5):
        vector_scores = {
            result["content"]: float(result["_additional"]["score"])
            for result in vector_results
        }
        keyword_scores = {
            result["content"]: float(result["_additional"]["score"])
            for result in keyword_results
        }

        all_contents = list(set(vector_scores.keys()).union(keyword_scores.keys()))
        combined_scores = {}

        for content in all_contents:
            vec_score = vector_scores.get(content, 0)
            key_score = keyword_scores.get(content, 0)

            """ test: get the score """
            # print("vec: " + str(vec_score))
            # print("key: " + str(key_score))


            combined_score = alpha * vec_score + (1 - alpha) * key_score
            combined_scores[content] = combined_score

        sorted_combined_scores = sorted(
            combined_scores.items(), key=lambda x: x[1], reverse=True
        )
        top_results = [item[0] for item in sorted_combined_scores[:num_results]]
        return top_results


def main(file_path):
    df = pd.read_excel(file_path)
    questions = df["問題"].tolist()
    answers = df["答案"].tolist()

    """ for test mode"""
    # questions = questions[0:30]
    # answers = answers[0:30]

    searcher = WeaviateSemanticSearch(config.get("Weaviate", "classnm"))
    results = []

    for question, answer in zip(questions, answers):
        """中研院 CKIP 分詞"""
        # ws = ws_driver([question])
        # pos = pos_driver(ws)
        # keyword = clean(ws[0], pos[0])

        """ LLM 分詞 """
        keyword = call_aied(question)
        print("keywords: " + keyword)

        vector_results = searcher.vector_search(question, 1000)
        keyword_results = searcher.keyword_search(keyword, 1000)
        for alpha in [round(x * 0.1, 1) for x in range(10, -1, -1)]:
            result = searcher.hybrid_search(
                vector_results, keyword_results, alpha, num_results=1
            )
            results.append(
                {
                    "問題": question,
                    "答案": answer,
                    "關鍵字": keyword,
                    f"檢索結果_{alpha}": result,
                }
            )

    result_df = pd.DataFrame(results)
    result_df.to_excel("result/test_1006/testresult_3493.xlsx", index=False)
    print("finished")


if __name__ == "__main__":
    main("result/test_1006/testdata_3493.xlsx")
    # main("result/backup/第二次試驗/【測試資料】_60題.xlsx")
