import numpy as np
import pandas as pd
from collections import Counter
from scipy.sparse import csr_matrix
from scipy.sparse import diags 

class SearchEngine:
    def __init__(self, corp_champ):
        self.corp_champ = corp_champ
        self.documents = list(corp_champ.documents.values())
        #self._construire() # vocab + mat_TF + mat_TFxIDF
        self.N = len(self.documents)
    

        frequences = Counter()
        document_frequency = Counter()


        for doc in self.corp_champ.documents.values():
            mots = self.corp_champ.nettoyer_texte(doc.texte).split()
            frequences.update(mots)
            
            document_frequency.update(set(mots))

        self.freq = pd.DataFrame({
            "mot": list(frequences.keys()),
            "term_frequency": list(frequences.values()),
            "document_frequency": [document_frequency[mot] for mot in frequences.keys()]
        })

        self.freq.sort_values('mot', ascending=True, inplace=True)   #df dans l'ordre des mots, meme si au début : nb et caractères spéciaux
        self.freq.reset_index(drop=True, inplace=True)
        #print(freq[:60])
        """
        vocab={}
        for index, row in freq.iterrows():
            
            mot = row['mot'] 
            
            # Stockage des informations dans un sous-dictionnaire
            vocab[mot] = {
                "identifant": index,
                "term_frequency": row['term_frequency'],      # Nom de colonne à adapter selon votre DataFrame
                "document_frequency": row['document_frequency']            # Nom de colonne à adapter selon votre DataFrame
            }
        #vocab = dict(sorted(vocab.items())) 
        vocab = dict(vocab.items())
        # #on aurait pu utiliser les variables qu'on a créer pour construire le DF (frequency), plus simple pour identifiants
        #déjà trié

        #print (vocab)
        """
        self.mots_vocab = list(self.freq["mot"])
        self.documents = list(corp_champ.documents.values())  
        self.mots_presents = {mot: i for i, mot in enumerate(self.mots_vocab)}#dictionnaire des mots avec id

        lignes = []
        colonnes = []
        valeurs = []


        #IA
        for i, doc in enumerate(self.documents):
            mots = self.corp_champ.nettoyer_texte(doc.texte).split() #obligé de refaire car pas le meme compte qu'avant : on compte par documents et pas dans tous le corpus
            compteur = Counter(mots)        #pas le meme ordre je crois
            #--->frequences c le compteur

            for j, mot in enumerate(self.mots_vocab):
                # 2. Vérifier la fréquence du mot dans CE document
                if compteur[mot] > 0:            
                    lignes.append(i)    
                    colonnes.append(j)
                    valeurs.append(compteur[mot])

        self.mat_TF = csr_matrix(
            (valeurs, (lignes, colonnes)),
            shape=(len(self.documents), len(self.mots_vocab))
        )
        #fin IA
        #print(mat_TF)


        #N=len(corp_champ.documents.values())
        self.idf=np.log(self.N/self.freq['document_frequency'])
        self.freq["idf"]=self.idf
        self.freq["tf-idf"]=self.freq["idf"]*self.freq['term_frequency']
        #print (freq.head())

        self.mat_TFxIDF = self.mat_TF @ diags(self.idf)
        #print ("TF-IDF", mat_TFxIDF)
        self.normes_docs = np.sqrt(np.asarray(self.mat_TFxIDF.multiply(self.mat_TFxIDF).sum(axis=1)).ravel())



    #requete = input("Que recherchez-vous ? ")

    def search(self, requete, top_n=5):
        mots_rq = self.corp_champ.nettoyer_texte(requete).split()

        #vocab = dict(vocab.items())

        # Construire le vecteur TF de la requête
        vecteur = np.zeros(len(self.mots_vocab))#tableau de 0 de taille mot_vocab
        for mot in mots_rq:
            if mot in self.mots_presents:
                vecteur[self.mots_presents[mot]] += 1

        # Appliquer les poids IDF
        vecteur = vecteur * self.idf

        # Calculer les cosinus avec chaque document
        produits = self.mat_TFxIDF @ vecteur
        
        #IA
        norme_requete = np.linalg.norm(vecteur)
        print ("\n\n\n norme requete :", norme_requete)

        scores = np.zeros(len(produits))#tab 0 de taille tf idf+vecteur(mots, 1)
        if norme_requete != 0:
            denominateurs = self.normes_docs * norme_requete
            scores = np.divide(
                produits.ravel(),
                denominateurs,
                out=np.zeros_like(self.normes_docs, dtype=float),
                where=denominateurs != 0
            )

        #fin IA 


        # Trier et afficher les 5 meilleurs documents
        #documents = list(corp_champ.documents.values())
        ordre = np.argsort(scores)[::-1]

        resultats_data = []
        for i in ordre[:top_n]:
            if scores[i] > 0:
                resultats_data.append({
                    "score": scores[i],
                    "titre": self.documents[i].titre,
                    "document": self.documents[i]
                })
        return pd.DataFrame(resultats_data)
  

