import dspy
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from utils.qdrant_strm import QdrantSTRM
from utils.react_custom import ReActCustom

llm = dspy.AzureOpenAI(
    api_base="",
    api_version="",
    model="gpt-35-turbo-16k",
    api_key="",
    deployment_id="gpt-35-turbo-16k",
    max_tokens=100,
)
client = QdrantClient(path="base")
encoder = SentenceTransformer("maidalun1020/bce-embedding-base_v1", token="")
retriever = QdrantSTRM("test_0615", client, encoder, k=5)
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
