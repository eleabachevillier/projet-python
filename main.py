

import os
import praw #faire uv praw das la console
import urllib
import urllib.request
import xmltodict




"""

#uv add arxiv
#
import numpy as np
import json
import pickle
import datetime
import pandas as pd



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
for post in posts:
    # Titre toujours présent
    texte = post.title.replace("\n", " ") + ". " #on récupere les titres

#Contenu textuel
    if post.selftext: #si le poste contient du texte
        texte += post.selftext.replace("\n", " ") #titres+contenu
    elif post.url:
        texte += post.url   #titre}url

    docs.append(texte) #mettre dans liste



for texte in docs[:5]: #affiher 5 premiers elem de la liste
    print("\n---")
    print(texte)

#exit()


#1.2
#« Merci à arXiv pour l’utilisation de son interopérabilité en libre accès. »

url = 'https://export.arxiv.org/api/query?search_query=all:tree&start=0&max_results=5' 



data = urllib.request.urlopen(url) #on appel l'API, permet de faire une requette HTTP
donnees=(data.read().decode('utf-8'))
print (donnees)

resultat = xmltodict.parse(donnees)
docs.append(resultat)
print(docs)



