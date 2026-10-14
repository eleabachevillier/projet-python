import pandas as pd
from Author import Author
import re 


def singleton(cls):
    instance = [None]
    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]
    return wrapper


@singleton
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
            
            for doc_id, doc in documents_tries[:5]:
                print(doc)
    #fin IA

    def trie_titre(self, doc):
                documents_tries = sorted(
                self.documents.items(),
                key=lambda x: x[1].titre
                )
                
                for doc_id, doc in documents_tries[:5]:
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
        return f"Corpus (nom='{self.nom}')"


    """  
    def search(self, mot):
        texte = self.texte_complet() # cache
        return re.findall(r"[^.]*\b" + mot + r"\b[^.]*", texte, re.IGNORECASE)    
    """     
    #def search(self, mot):
         #ia : au premier appel, chaine_join est créée et conservée dans self, Aux appels suivants, elle est réutilisée sans être reconstruite.
   # if not hasattr(self, "chaine_join"):
        #self.texte = self.texte_complet()
        #return re.findall(r"[^.]*\b" + re.escape(mot) + r"\b[^.]*",self.texte,re.IGNORECASE
    #)
    def search(self, mot):
        if not hasattr(self, "chaine_join"):
           # haine_join=" ".join(
            self.chaine_join = " ".join(
                doc.texte for doc in self.documents.values()
            )
            #return self.chaine_join
    
        return re.findall(
            r"[^.]*\b" + re.escape(mot) + r"\b[^.]*",
            self.chaine_join,
            re.IGNORECASE
        )

    def concordancier (self, mot):
         search(self, mot)
     
     