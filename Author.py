class Author :

    def __init__(self, name):
        self.name = name
        self.nb_docs = 0
        self.production = {}

    def add(self, doc_id, doc):
        self.production[doc_id] = doc
        self.nb_docs += 1


    def __str__(self):
        return f"l'auteur est : {self.name} et son nombre de documents est : {self.nb_docs} "