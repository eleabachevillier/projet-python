
import os
import praw #faire uv praw das la console
import urllib
import urllib.request
import xmltodict
import pandas as pd



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
"""
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


for post in posts:
    # Titre toujours présent
    texte = post.title.replace("\n", " ") + ". " #on récupere les titres

#Contenu textuel
    if post.selftext: #si le poste contient du texte
        texte += post.selftext.replace("\n", " ") #titres+contenu
    elif post.url:
        texte += post.url   #titre}url

    docs.append(texte) #mettre dans liste
    origines.append('reddit')



"""
"""
for texte in docs[:5]: #affiher 5 premiers elem de la liste
    print("\n---")
    print(texte)
    #exit()
"""
#1.2
#« Merci à arXiv pour l’utilisation de son interopérabilité en libre accès. »

"""

url = 'https://export.arxiv.org/api/query?search_query=all:tree&start=0&max_results=5' 



data = urllib.request.urlopen(url) #on appel l'API, permet de faire une requette HTTP
donnees=(data.read().decode('utf-8'))


resultat = xmltodict.parse(donnees) #en liste

for article in resultat["feed"]["entry"] : #on se balade dans l'arbre, on veut le texte uniquement
        docs.append(article["summary"])
        origines.append("Arxiv")


######################Partie 2 : 
#2.1
id=[]
for i in range (len(docs)) :
        id.append(i)
df=pd.DataFrame({ "identifiant ": id, "text" : docs, "origine": origines})
#print(df)

##2.2
df.to_csv('articles_tree.csv', sep='\t', index=False)
"""
#2.3

df_tree=pd.read_csv('articles_tree.csv', sep='\t')



#####################Partie 3 :

#3.1
taille=(len(df_tree))

#3.2
for ligne in df_tree['text'] :
    """
    mot = ligne.split(" ")
    print('mot',len(mot))

    phrases=ligne.split(".")
    print('phrases',len(phrases))
    """
    #print('caractère',len(ligne),'\n')
    
#3.3
for i, ligne in enumerate(df_tree['text']): #pour ajouter ligne par ligne
   df_tree.loc[i, "nb_caracteres"] = len(ligne)


df_tree=df_tree[df_tree["nb_caracteres"]>=100]
print(df_tree)

#3.4
chaine_join=" ".join([ligne for ligne in df_tree['text']])
print(chaine_join)
