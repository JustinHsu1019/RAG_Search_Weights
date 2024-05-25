import dspy
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_strm import QdrantSTRM
from react_custom import ReActCustom
# import langchain

#llm = dspy.Cohere(api_key="")
llm = dspy.AzureOpenAI(
    api_base="",
    api_version="",
    model="gpt-35-turbo-16k",
    api_key="",
    deployment_id="gpt-35-turbo-16k",
    max_tokens=500,
)
client = QdrantClient(path="bce_base_no_chunking")
encoder = SentenceTransformer("maidalun1020/bce-embedding-base_v1", token="")
retriever = QdrantSTRM("test_0424", client, encoder, k=5)
dspy.settings.configure(lm=llm, rm=retriever)

agent = ReActCustom("question -> answer_zh_tw")

while True:
    question = input("Question: ")
    print()
    result = agent.forward(question=question)
    print("Answer:")
    print(result.answer_zh_tw)
    print("History:")
    llm.inspect_history(5)
