
import os
import praw #faire uv praw das la console
import urllib
import urllib.request
import xmltodict
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter
from scipy.sparse import csr_matrix
from scipy.sparse import diags

from Document import Document
from Author import Author
from Corpus import Corpus
from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument
from DocumentFactory import Fabrique


"""

#uv add arxiv
#




"""

##############################   PARTIE I :   ##################
############Partie 1 :

#1.1
corp_champ= Corpus ("Dans les champs")


taille_docs=100
#Récupération de textes depuis Reddit
reddit = praw.Reddit(
    client_id='m4W3R1MLvrnNI9LTbG35Eg', 
    client_secret='ynb_xt5pKo4IFhssuuqr5ENTMu5Q4g', 
    user_agent='Walid_M1'
) #connexion à une API

subr = reddit.subreddit('tree')
posts = list(subr.hot(limit=taille_docs))#les articles principaux sur le domaine choisi (contenu)


docs = []
origines = []
documents={}
i=0
authors = {}



for post in posts:
    # Titre toujours présent
    titre = post.title #on récupere les titres
    auteur = post.author #str( ) 
    date = datetime.fromtimestamp(post.created_utc)
    url=post.url
    texte = post.selftext.replace("\n", " ")
    num_comments= post.num_comments 

    docs.append(texte) #mettre dans liste
    origines.append('reddit')
    
    c_documents = Document (titre,auteur,date,url,texte)#instanciation 
    doc_Reddit=RedditDocument (titre,auteur,date,url,texte, num_comments)
    corp_champ.add (doc_Reddit)
    #documents[i]=c_documents#dictionnaire 
    documents[i]=doc_Reddit
    i=i+1    
    
    if auteur not in authors : ##on fait en 2 fois car plusieurs auteurs pour arxiv et bug
            authors[auteur] = Author(auteur) #on met l'instance en value de la key auteur (auteur correspondant à l'instance)
    
    authors[auteur].add(i, c_documents)
   
    

   
    


"""
for texte in docs[:5]: #affiher 5 premiers elem de la liste
    print("\n---")
    print(texte)
    #exit()
"""
#1.2
#« Merci à arXiv pour l’utilisation de son interopérabilité en libre accès. »



url = 'https://export.arxiv.org/api/query?search_query=all:tree&start=0&max_results=100'

data = urllib.request.urlopen(url)  # on appel l'API, permet de faire une requette HTTP
donnees = data.read().decode('utf-8')

resultat = xmltodict.parse(donnees)  # en liste

for article in resultat["feed"]["entry"]:  # on se balade dans l'arbre, on veut le texte uniquement
    titre = article["title"]
    auteurs_article = article["author"]
    #date = datetime.fromtimestamp(article["published"])  
    date = datetime.fromisoformat(article["published"].replace("Z", ""))
    url = article["id"]
    texte = article["summary"]

    if isinstance(auteurs_article, dict):
        auteurs_article = [auteurs_article]

    for a in auteurs_article :
        noms = a["name"]
    auteur = noms[0]
    coauteurs = noms[1:]
    #noms = [a["name"] for a in auteurs_article] #pour mettre dans auteur et dans les coauteurs
    #auteur = noms[0]
    #coauteurs = noms[1:]
    

    doc_Arxiv = ArxivDocument(titre,auteurs_article, date, url, texte,coauteurs)#coauteurs
    c_documents2 = Document(titre,auteurs_article, date, url, texte)
    # #auteur article est une liste (ou un dictionnaire)
    documents[i] = c_documents2  # dictionnaire
    i = i + 1


    docs.append(texte)
    origines.append("Arxiv")
    corp_champ.add(doc_Arxiv)

    if isinstance(auteurs_article, dict):
        auteurs_article = [auteurs_article]

    for nom in auteurs_article:
        auteur = nom["name"]

        if auteur not in authors:
            authors[auteur] = Author(auteur)
                 
        authors[auteur].add(i, c_documents)
       

    
 

######################Partie 2 : 
    #2.1

id=[]
for i in range (len(docs)) :
        id.append(i)
df=pd.DataFrame({ "identifiant ": id, "text" : docs, "origine": origines})
print(df)

##2.2
df.to_csv('articles_tree.csv', sep='\t', index=False)

#2.3


df_tree=pd.read_csv('articles_tree.csv', sep='\t')



#####################Partie 3 :

#3.1
taille=(len(df_tree))
print (f"taille du corpus : {taille}") ##############verif que fonctionne

#3.2
for ligne in df_tree['text'] :   
    if pd.notna(ligne):  # Vérifie si la ligne n'est pas vide
        mot = ligne.split(" ")
        #print('mot',len(mot))

        phrases=ligne.split(".")
        #print('phrases',len(phrases))
    #else:
        #print('ligne vide')


    #print('caractère',len(ligne),'\n')
    
#3.3
for i, ligne in enumerate(df_tree['text']): #pour ajouter ligne par ligne
    if pd.notna(ligne):
        df_tree.loc[i, "nb_caracteres"] = len(ligne)
    else:
        df_tree.loc[i, "nb_caracteres"] = 0



df_tree=df_tree[df_tree["nb_caracteres"]>=100]
#print(df_tree)


#3.4
#chaine_join=" ".join([ligne for ligne in df_tree['text']])
#print(chaine_join)



    ################Partie 4 :
    #4.2 /4.3

#print (f"toutes les informations de l'instance \n : titre {c_documents.titre}, auteur {c_documents.auteur}, date {c_documents.date}, url {c_documents.url}, texte {c_documents.texte}'\n")
#print (f"toutes les informations de l'instance \n : titre {doc_Reddit.titre}, auteur {doc_Reddit.auteur}, date {doc_Reddit.date}, url {doc_Reddit.url}, texte {doc_Reddit.texte}, nb_com {num_comments}'\n")

print (documents[1])
print("Nombre de documents :", len(documents))

    ################Partie 5 :
    #5.2 /5.3


#for nom, auteur in authors.items():
#    print(nom, ":", auteur.nb_docs, "documents") 

 ####5.4 
"""
nom_recherche=input("Entrez le nom de l'auteur à rechercher : ")
if nom_recherche in authors:
     auteur = authors[nom_recherche]
     print("Nombre de documents produits :", auteur.nb_docs)
if nom_recherche not in authors:
     print ("pas trouvé")
"""


#print("id doc : ",corp_champ.id_documents)#nb docs dans le corpus selectionné
#marche avec reddit

print (corp_champ.trie_date(corp_champ))
#print (corp_champ.trie_titre(corp_champ)) 




corp_champ.save_fichier("corpus_article.csv")

#corp_champ.load_fichier("corpus_article.csv")
#corpus=pd.read_csv('corpus_article.csv', sep='\t')
#print (corpus)



print(doc_Reddit.getType())
doc_Arxiv.getType()

#print(Corpus() is Corpus())

doc_fab = Fabrique.document_factory("arxiv", titre, auteur, date, url, texte,
                       coauteurs=["Alice", "Bob"])
#corp_champ.add(doc_fab)

"""
recherche = corp_champ.search("cold")
print (f"le texte qu'on veut est {recherche}\n\n présentation")

resultats = corp_champ.concorde("cold", 30)
print (resultats)

print("\n cold 2 : \n\n")
resultats2 = corp_champ.concorde("cold", 50)
print (resultats2)
print("\n\ntree : \n\n")
resultats3 = corp_champ.concorde("tree", 30)
print (resultats3.head())
"""

"""
vocab1 = set()
for doc in corp_champ.documents.values():
    vocab1.update(corp_champ.nettoyer_texte(doc.texte).split())

vocab1 = sorted(vocab1)

"""
frequences = Counter()
document_frequency = Counter()


for doc in corp_champ.documents.values():
    mots = corp_champ.nettoyer_texte(doc.texte).split()
    frequences.update(mots)
    
    document_frequency.update(set(mots))

freq = pd.DataFrame({
    "mot": list(frequences.keys()),
    "term_frequency": list(frequences.values()),
    "document_frequency": [
        document_frequency[mot] for mot in frequences.keys()
    ]
})

freq.sort_values('mot', ascending=True, inplace=True)   #df dans l'ordre des mots, meme si au début : nb et caractères spéciaux
print(freq[:60])


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

mots_vocab = list(freq["mot"])

documents = list(corp_champ.documents.values())  

lignes = []
colonnes = []
valeurs = []

for doc in corp_champ.documents.values():
    mots = corp_champ.nettoyer_texte(doc.texte).split()
    frequences.update(mots)
    
    document_frequency.update(set(mots))


#IA
for i, doc in enumerate(documents):
    mots = corp_champ.nettoyer_texte(doc.texte).split() #obligé de refaire car pas le meme compte qu'avant : on compte par documents et pas dans tous le corpus
    compteur = Counter(mots)        #pas le meme ordre je crois
    #--->frequences c le compteur

    for j, mot in enumerate(mots_vocab):
        # 2. Vérifier la fréquence du mot dans CE document
        if compteur[mot] > 0:        
            lignes.append(i)
            colonnes.append(j)
            valeurs.append(frequences[mot])

mat_TF = csr_matrix(
    (valeurs, (lignes, colonnes)),
    shape=(len(documents), len(mots_vocab))
)
#fin IA
#print(mat_TF)


N=len(corp_champ.documents.values())

idf=np.log(N/freq['document_frequency'])
freq["idf"]=idf
freq["tf-idf"]=freq["idf"]*freq['term_frequency']
print (freq.head())

mat_TFxIDF = mat_TF @ diags(idf)
print ("TF-IDF", mat_TFxIDF)
