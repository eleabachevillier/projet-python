
import os
import praw #faire uv praw das la console
import urllib
import urllib.request
import xmltodict
import pandas as pd
from datetime import datetime

from Document import Document
from Author import Author

"""

#uv add arxiv
#


import numpy as np
import json

import datetime




"""

##############################   PARTIE I :   ##################
############Partie 1 :

#1.1

taille_docs=10

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

    docs.append(texte) #mettre dans liste
    origines.append('reddit')

    c_documents = Document (titre,auteur,date,url,texte)#instanciation 
    documents[i]=c_documents#dictionnaire 
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



url = 'https://export.arxiv.org/api/query?search_query=all:tree&start=0&max_results=5'

data = urllib.request.urlopen(url)  # on appel l'API, permet de faire une requette HTTP
donnees = data.read().decode('utf-8')

resultat = xmltodict.parse(donnees)  # en liste

for article in resultat["feed"]["entry"]:  # on se balade dans l'arbre, on veut le texte uniquement
    titre = article["title"]
    date = article["published"]
    auteurs_article = article["author"]
    url = article["id"]
    texte = article["summary"]

    c_documents2 = Document(titre,auteurs_article, date, url, texte)#
    documents[i] = c_documents2  # dictionnaire
    i = i + 1

    """
    for auteur in auteurs_article:
        nom = auteur["name"]

        if nom not in authors:
            authors[nom] = Author(nom)
       
        authors[nom].add(i, c_documents)
   """     

    docs.append(texte)
    origines.append("Arxiv")

######################Partie 2 : 
    #2.1
"""
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

    #3.2
    for ligne in df_tree['text'] :   
        if pd.notna(ligne):  # Vérifie si la ligne n'est pas vide
            mot = ligne.split(" ")
            print('mot',len(mot))

            phrases=ligne.split(".")
            print('phrases',len(phrases))
        else:
            print('ligne vide')


        #print('caractère',len(ligne),'\n')
        
    #3.3
    for i, ligne in enumerate(df_tree['text']): #pour ajouter ligne par ligne
        if pd.notna(ligne):
            df_tree.loc[i, "nb_caracteres"] = len(ligne)
        else:
            df_tree.loc[i, "nb_caracteres"] = 0



    df_tree=df_tree[df_tree["nb_caracteres"]>=100]
    print(df_tree)


    #3.4
    chaine_join=" ".join([ligne for ligne in df_tree['text']])
    #print(chaine_join)
"""


    ################Partie 4 :
    #4.2 /4.3
    print (f"toutes les informations de l'instance \n : titre {c_documents.titre}, auteur {c_documents.auteur}, date {c_documents.date}, url {c_documents.url}, texte {c_documents.texte}'\n")

    print("manière avec __str__"\n)
    print (documents[1])
    print("Nombre de documents :", len(documents))

    ################Partie 5 :
    #5.2 /5.3


"""
for doc_id,document in documents.items():
    nom=documents[doc_id].auteur
    if nom not in authors :
        authors[nom] = Author(nom) #on met l'instance en value de la key nom (nom correspondant à l'instance)

    authors[nom].add(doc_id, document)


for nom, auteur in authors.items():
    print(nom, ":", auteur.nb_docs, "documents")     
"""
for nom, auteur in authors.items():
    print(nom, ":", auteur.nb_docs, "documents")     

####5.4