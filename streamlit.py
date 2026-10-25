import streamlit as st
import pandas as pd
from tqdm import tqdm


from Document import Document
from Corpus import Corpus
from SearchEngine import SearchEngine


#on reconstruit le corpus pour cette nouvelle interface 
#ensuite on appel de nouveau SearchCorpus pour trouver les documents 
corpus_art=pd.read_csv('corpus_article.csv', sep=',')
corp_champ = Corpus("Nature and tree")

for index, row in corpus_art.iterrows():
    document = Document(
        str(row["titre"]), 
        str(row["auteur"]), 
        str(row["date"]), 
        str(row["url"]), 
        str(row["texte"])
    )
    corp_champ.add(document)
#pour ne pas construire la matrice à chaque fois
@st.cache_resource
def charger_matrice():
    return SearchEngine(corp_champ)

arbre = charger_matrice()



st.title("Moteur de recherche")
st.header('theme : tree')

rq = st.text_input('Entrez votre requête')
nb_doc=st.slider('Nombre de documents à afficher : ', 0, 15)



if st.button("Rechercher"):
    resultats= arbre.search(rq, top_n=nb_doc)
    if not resultats.empty:
            #on veut convertir en texte pour le plus utiliser "document"--> avant ça fonctionnait mais on avait des messages d'erreur dansle terminal
                #.to_string() ne fonctionne pas
                #IA
                # Si la colonne 'titre' contient l'objet Document, on extrait son vrai titre textuel :
                if 'titre' in resultats.columns:
                    resultats['titre'] = resultats['titre'].apply(
                        lambda x: x.titre if hasattr(x, 'titre') else str(x)
                    )
                #Fin IA

    st.dataframe(resultats)
