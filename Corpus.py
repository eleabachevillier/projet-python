import pandas as pd
from Author import Author
import re 
import pandas as pd


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


    def texte_complet(self):
        return " ".join(
            doc.texte for doc in self.documents.values()
        )

    def texte_cache(self):
        if not hasattr(self, "chaine_join"):
            self.chaine_join = self.texte_complet()
        return self.chaine_join




    def search(self, mot):
        texte = self.texte_cache()
        return re.findall(r"[^.]*\b" + mot + r"\b[^.]*", texte, re.IGNORECASE)#enleve points, tous dès 0 , un grp de mot 


   #IA
    def concorde(self, mot, taille_contexte=30):
        """
        Construit un concordancier pour une expression donnée.
        
        Paramètres :
        - expression (str) : Le mot ou l'expression régulière à rechercher.
        - taille_contexte (int) : Le nombre de caractères à inclure pour le contexte 
          de gauche et de droite (par défaut : 30).
          
        Retour :
        - pandas.DataFrame : Un tableau contenant les colonnes 
          'contexte_gauche', 'mot' et 'contexte_droite'.
        """
        texte = self.texte_cache()
        lignes = []
        pattern = r"\b" + mot + r"\b"

        # re.finditer permet de parcourir toutes les occurrences avec leurs positions (span)
        for match in re.finditer(pattern, texte, re.IGNORECASE):
            
            debut, fin = match.span()
            mot = match.group(0)

            # Extraction du contexte de gauche (en s'assurant de ne pas dépasser 0)
            debut_gauche = max(0, debut - taille_contexte)
            contexte_gauche = texte[debut_gauche:debut]

            # Extraction du contexte de droite (en s'assurant de ne pas dépasser la fin du texte)
            fin_droite = min(len(texte), fin + taille_contexte)
            contexte_droite = texte[fin:fin_droite]

            # Stockage des éléments dans une liste de dictionnaires
            lignes.append({
                "contexte_gauche": contexte_gauche,
                "mot": mot,
                "contexte_droite": contexte_droite
            })

        # Création et retour du DataFrame pandas
        return pd.DataFrame(lignes)
     #fin IA

    def nettoyer_texte(self, chaine):
        chaine = chaine.lower()
        chaine = chaine.replace("\n", " ")
        #chaine = re.sub(r"[0-9]+", " ", chaine) # supprimer les chiffres ????
        chaine = re.sub(r"[^\w\s]", " ", chaine) # ponctuation
        return re.sub(r"\s+", " ", chaine).strip()

    