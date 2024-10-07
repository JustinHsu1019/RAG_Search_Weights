import nltk
nltk.data.path.append('/Users/justin.hsu/nltk_data')
nltk.download('punkt_tab')

from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize

document1 = """
多爾、美國多爾、規、則、規則、美國、鳥類學家協會、鳥類學家協會規則、鳥類、多、協會、美、國
多爾鳥類學家協會、多爾鳥類、美國多爾鳥類學家、美國協會、多爾鳥、多爾協會
這是一個協會，這個協會在美國
這是一個專家，這個專家在美國
"""
document2 = """
自然環境指地球或一些區域上一切生命和非生命的事物以自然的狀態呈現。這是一個環境涵蓋了所有生物之間的相互作用。自然環境是對比建成環境，建成環境當中包括區域和組件受人類的強烈影響。一個地理區域被認為是一個自然的環境。發現完全自然的環境是困難的，並且自然度有連續的變化是常見的，有從一個極端的0％的自然度，到另一極端理想的100％的純自然度。更確切地說，我們能夠考慮環境的不同方面或組成部分，看到它們的的自然度並不均勻。例如，如果我們以農田為例，並考慮其礦物學成分和土壤結構，我們會發現，而前者是非常相似的未受干擾的林地土壤，但其結構是相當的不同。自然環境是經常被用來作為棲息地的同義字。例如，當我們說長頸鹿的自然環境是熱帶稀樹草原。地球科學普遍認同有4個領域，岩石圈，水圈，大氣，生物圈，對應於岩石，水，空氣和生命。構成及影響自然環境的物質種類很多。主要有空氣、水、植物、動物、土壤、岩石礦物、太陽輻射等。
"""
documents = [document1, document2]

tokenized_documents = [word_tokenize(doc.lower()) for doc in documents]

bm25 = BM25Okapi(tokenized_documents)

question = """
多爾規則 美國鳥類學家協會 動物 學名 命名法則
"""

tokenized_question = word_tokenize(question.lower())

scores = bm25.get_scores(tokenized_question)

for i, score in enumerate(scores):
    print(f"Document {i+1} Score: {score}")
