import weaviate
from langchain.embeddings import OpenAIEmbeddings
import sys
import os
import json
import warnings
import pandas as pd
from contextlib import redirect_stdout, redirect_stderr

from utils.ckip import ws_driver, pos_driver, clean
from utils.call_ai import call_aied
import utils.config_log as config_log


config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

wea_url = config.get("Weaviate", "weaviate_url")
PROPERTIES = ["uuid", "content"]

os.environ["OPENAI_API_KEY"] = config.get("OpenAI", "api_key")

# 忽略所有的 DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


def silent_call_ckip_v2(question):
    # 保存當前的 sys.stdout 和 sys.stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    try:
        # 使用 with 確保 stdout 和 stderr 正確地關閉，靜默所有輸出
        with open(os.devnull, "w") as fnull:
            with redirect_stdout(fnull), redirect_stderr(fnull):
                ws = ws_driver([question])
                pos = pos_driver(ws)
    finally:
        # 恢復 sys.stdout 和 sys.stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
    return ws, pos


class WeaviateSemanticSearch:
    def __init__(self, classNm, keyclassNm):
        self.url = wea_url
        self.embeddings = OpenAIEmbeddings(chunk_size=1, model="text-embedding-3-large")
        self.client = weaviate.Client(url=wea_url)
        self.classNm = classNm
        self.keyclassNm = keyclassNm

    def vector_search(self, query_text, num_results=185):
        query_vector = self.embeddings.embed_query(query_text)
        vector_str = ",".join(map(str, query_vector))

        gql_query = f"""
        {{
            Get {{
                {self.classNm}(hybrid: {{query: "{query_text}", vector: [{vector_str}], alpha: 1 }}, limit: {num_results}) {{
                    uuid
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

    def keyword_search(self, query_text, num_results=185):
        gql_query = f"""
        {{
            Get {{
                {self.keyclassNm}(hybrid: {{query: "{query_text}", vector: [], alpha: 0 }}, limit: {num_results}) {{
                    uuid
                    content
                    _additional {{
                        score
                    }}
                }}
            }}
        }}
        """
        search_results = self.client.query.raw(gql_query)
        results = search_results["data"]["Get"][self.keyclassNm]
        return results

    def hybrid_search(self, vector_results, keyword_results, alpha, num_results=3):
        vector_scores = {
            result["uuid"]: float(result["_additional"]["score"])
            for result in vector_results
        }
        keyword_scores = {
            result["uuid"]: float(result["_additional"]["score"])
            for result in keyword_results
        }

        all_ids = set(vector_scores.keys()).union(keyword_scores.keys())
        combined_scores = {}

        for doc_id in all_ids:
            vec_score = vector_scores.get(doc_id, 0)
            key_score = keyword_scores.get(doc_id, 0)

            """ test: score log """
            # print("vec: " + str(vec_score))
            # print("key: " + str(key_score))

            combined_score = alpha * vec_score + (1 - alpha) * key_score
            combined_scores[doc_id] = combined_score

        sorted_combined_scores = sorted(
            combined_scores.items(), key=lambda x: x[1], reverse=True
        )
        top_ids = [item[0] for item in sorted_combined_scores[:num_results]] # 第一個值是 最高分的結果

        return top_ids


def main(file_path, batch_size=100):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    qids = [item["qid"] for item in data]
    questions = [item["question"] for item in data]
    answers = [item["parentqid"] for item in data]

    """ get keyword from excel """
    # keywords = df["keyword"].tolist()

    """ for test mode"""
    # questions = questions[0:30]
    # answers = answers[0:30]
    # keywords = keywords[0:30]
    # batch_size = 10

    searcher = WeaviateSemanticSearch(
        config.get("Weaviate", "classnm"), config.get("Weaviate", "keyclassnm")
    )
    results = []
    # keyword_results = []

    for idx, (question, answer, qid) in enumerate(
        zip(questions, answers, qids)
    ):
        try:
            """ 中研院 CKIP 分詞 (目前使用中；但有過去數據就先直接使用，速度快) """
            ws = ws_driver([question])
            pos = pos_driver(ws)

            ws, pos = silent_call_ckip_v2(question)
            keyword = clean(ws[0], pos[0])

            """ LLM 分詞 (已棄用) """
            # keyword = call_aied(question)

            # keyword_results.append({
            #     '問題': question,
            #     '答案': answer,
            #     'keyword': keyword,
            #     'keyword_num': len(keyword.split())
            # })

            vector_results = searcher.vector_search(question, 185)
            keyword_results_search = searcher.keyword_search(keyword, 185)
            for alpha in [round(x * 0.1, 1) for x in range(10, -1, -1)]:
                result = searcher.hybrid_search(
                    vector_results, keyword_results_search, alpha, num_results=3
                )
                print(qid)
                print(result)
                print(question)
                print(answer)
                print(keyword)
                print("============================")
                results.append(
                    {
                        "QID": qid,
                        "問題": question,
                        "答案": answer,
                        "關鍵字": keyword,
                        f"檢索結果_{alpha}": result,
                    }
                )

            if (idx + 1) % batch_size == 0:
                result_df = pd.DataFrame(results)
                result_file = "result/test_1210/testresult_185_top3.xlsx"
                if os.path.exists(result_file):
                    existing_df = pd.read_excel(result_file)
                    result_df = pd.concat([existing_df, result_df], ignore_index=True)
                result_df.to_excel(result_file, index=False)
                results = []

                # keyword_df = pd.DataFrame(keyword_results)
                # keyword_file = "result/test_1006/testkey_3493.xlsx"
                # if os.path.exists(keyword_file):
                #     existing_keyword_df = pd.read_excel(keyword_file)
                #     keyword_df = pd.concat([existing_keyword_df, keyword_df], ignore_index=True)
                # keyword_df.to_excel(keyword_file, index=False)
                # keyword_results = []

        except Exception as e:
            logger.error(f"Error processing question {idx + 1}: {e}")

    if results:
        result_df = pd.DataFrame(results)
        result_file = "result/test_1210/testresult_185_top3.xlsx"
        if os.path.exists(result_file):
            existing_df = pd.read_excel(result_file)
            result_df = pd.concat([existing_df, result_df], ignore_index=True)
        result_df.to_excel(result_file, index=False)

    # if keyword_results:
    #     keyword_df = pd.DataFrame(keyword_results)
    #     keyword_file = "result/test_1006/testkey_3493.xlsx"
    #     if os.path.exists(keyword_file):
    #         existing_keyword_df = pd.read_excel(keyword_file)
    #         keyword_df = pd.concat([existing_keyword_df, keyword_df], ignore_index=True)
    #     keyword_df.to_excel(keyword_file, index=False)

    print("finished")


if __name__ == "__main__":
    main("data/question.json")
    # main("result/backup/第二次試驗/【測試資料】_60題.xlsx")
