import math
from collections import Counter
from typing import List
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger


class BM25F:
    def __init__(self, documents: List[str], k1=1.5, b=0.75):
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.doc_lens = [len(doc) for doc in documents]
        self.avg_doc_len = sum(self.doc_lens) / len(documents)
        self.N = len(documents)
        self.ws_driver = None
        self.pos_driver = None
        self._initialize_ckip_drivers()
        self.doc_freqs = self._compute_doc_frequencies()

    def _initialize_ckip_drivers(self):
        if not self.ws_driver or not self.pos_driver:
            self.ws_driver = CkipWordSegmenter(model="albert-base")
            self.pos_driver = CkipPosTagger(model="albert-base")

    def _tokenize(self, text: str) -> List[str]:
        ws = self.ws_driver([text])
        pos = self.pos_driver(ws)
        return self._clean(ws[0], pos[0])

    def _clean(self, sentence_ws, sentence_pos):
        short_sentence = []
        stop_pos = set(["Nep", "Nh", "Nb"])
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            is_N_or_V = word_pos.startswith("V") or word_pos.startswith("N")
            is_not_stop_pos = word_pos not in stop_pos
            is_not_one_character = not (len(word_ws) == 1)
            if is_N_or_V and is_not_stop_pos and is_not_one_character:
                short_sentence.append(word_ws)
        return short_sentence

    def _compute_doc_frequencies(self):
        df = Counter()
        for doc in self.documents:
            tokens = set(self._tokenize(doc))
            df.update(tokens)
        return df

    def score(self, query: str, document: str) -> float:
        query_tokens = self._tokenize(query)
        doc_tokens = self._tokenize(document)
        doc_len = len(doc_tokens)
        tf = Counter(doc_tokens)

        score = 0.0
        for token in query_tokens:
            df = self.doc_freqs.get(token, 0)
            if df == 0:
                continue
            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)
            tf_token = tf[token]
            denom = tf_token + self.k1 * (
                1 - self.b + self.b * (doc_len / self.avg_doc_len)
            )
            score += idf * ((tf_token * (self.k1 + 1)) / denom)

        return score

    def rank(self, query: str) -> List[float]:
        return [self.score(query, doc) for doc in self.documents]

    def normalize_score(
        self, score: float, min_score: float, max_score: float
    ) -> float:
        if max_score == min_score:
            return 0.0
        return (score - min_score) / (max_score - min_score)

    def rank_normalized(self, query: str) -> List[float]:
        scores = self.rank(query)
        print(scores)
        min_score = min(scores)
        max_score = max(scores)
        return [self.normalize_score(score, min_score, max_score) for score in scores]


def main():
    documents = [
        """多爾、美國多爾、規、則、規則、美國、鳥類學家協會、鳥類學家協會規則、鳥類、多、協會、美、國
多爾鳥類學家協會、多爾鳥類、美國多爾鳥類學家、美國協會、多爾鳥、多爾協會
這是一個協會，這個協會在美國
這是一個專家，這個專家在美國""",
        "自然環境指地球或一些區域上一切生命和非生命的事物以自然的狀態呈現。這是一個環境涵蓋了所有生物之間的相互作用。自然環境是對比建成環境，建成環境當中包括區域和組件受人類的強烈影響。一個地理區域被認為是一個自然的環境。發現完全自然的環境是困難的，並且自然度有連續的變化是常見的，有從一個極端的0％的自然度，到另一極端理想的100％的純自然度。更確切地說，我們能夠考慮環境的不同方面或組成部分，看到它們的的自然度並不均勻。例如，如果我們以農田為例，並考慮其礦物學成分和土壤結構，我們會發現，而前者是非常相似的未受干擾的林地土壤，但其結構是相當的不同。自然環境是經常被用來作為棲息地的同義字。例如，當我們說長頸鹿的自然環境是熱帶稀樹草原。地球科學普遍認同有4個領域，岩石圈，水圈，大氣，生物圈，對應於岩石，水，空氣和生命。構成及影響自然環境的物質種類很多。主要有空氣、水、植物、動物、土壤、岩石礦物、太陽輻射等。",
    ]

    query = "多爾規則 美國鳥類學家協會 動物 學名 命名法則"

    bm25f = BM25F(documents)
    normalized_scores = bm25f.rank_normalized(query)

    for i, score in enumerate(normalized_scores):
        print(
            f"文案 {i + 1}: {documents[i][:50]}...\n相關性分數 (0~1 正規化): {score:.4f}\n"
        )


if __name__ == "__main__":
    main()
