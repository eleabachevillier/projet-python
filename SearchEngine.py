class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self._construire() # vocab + mat_TF + mat_TFxIDF
    def search(self, mots_clefs, n=5):