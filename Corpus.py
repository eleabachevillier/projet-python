import pandas as pd
from Author import Author


class Corpus : 
    "corpus de documents"

    def __init__(self, nom):
        self.nom = nom
        self.documents = {}
        self.id_documents = 0
        self.authors = {}

    def add(self, doc) :
        self.documents[self.id_documents] = doc

        doc_id = self.id_documents
        self.id_documents += 1

        #nom = doc.auteur
        
       # if isinstance(doc.auteur, dict):
         #   auteurs_article = [doc.auteur]
        #else:
             #auteurs_article = doc.auteur

       # for auteur in auteurs_article:
            #nom = auteur["name"] if isinstance(auteur, dict) else auteur
            
        #for nom in auteurs_article:
                #auteur = nom["name"]

      
        if isinstance(doc.auteur, dict):
            auteurs_article = [doc.auteur["name"]]
        elif isinstance(doc.auteur, list):
            auteurs_article = []
            for a in doc.auteur:
                if isinstance(a, dict):
                    auteurs_article.append(a["name"])
                else:
                    auteurs_article.append(a)
                                    
        else:
            auteurs_article = [doc.auteur]

        for nom in auteurs_article:
            if nom not in self.authors:
                self.authors[nom] = Author(nom)

            self.authors[nom].add(doc_id, doc)
           

        #if auteurs_article not in self.authors :

           # self.authors[nom] = Author(nom)

        #self.authors[nom].add(doc_id, doc)

    #def trie_date(self, doc):
       # documents_tries = sorted(
      # for 
            #document.date = sorted) <--on n'a pas les dates dans le meme dichoer et trie les dates, pas les docs...
    
    #IA  
    def trie_date(self, doc):
            documents_tries = sorted(
            self.documents.items(),
            key=lambda x: x[1].date
            )
            
            for doc_id, doc in documents_tries[:1]:
                print(doc)
    #fin IA

    def trie_titre(self, doc):
                documents_tries = sorted(
                self.documents.items(),
                key=lambda x: x[1].date
                )
                
                for doc_id, doc in documents_tries[:1]:
                    print(doc)

    def save_fichier(self, fichier):
        donnees = []
        for doc_id, doc in self.documents.items():
            donnees.append({
                "id": doc_id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte
                # df=pd.DataFrame({ "identifiant ": id, "text" : docs, "origine": origines})
            })
    
        df = pd.DataFrame(donnees)

        df.to_csv(fichier, index=False)
    
    #def load_fichier(fichier):
        corpus=pd.read_csv('articles_tree.csv', sep='\t')


    def __repr__(self):
        return f"le nom du corpus est : {self.nom}"