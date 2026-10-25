import streamlit as st
import pandas as pd
from SearchEngine import SearchEngine  # Assurez-vous que votre classe est bien accessible

st.title("Moteur de recherche")
st.header('theme : tree')
@st.cache_resource
def charger_matrice():
    SearchEngine(corp_champ)

new = charger_matrice()

rq = st.text_input('Entrez votre requête')

nb_docsss=st.slider('Nombre de documents à afficher : ', 0, 15)



if st.button("Rechercher"):
    test = rq
    st.write(f"resultats {test} et nb docs : bonjouuuuuuuuuuuuuuuuuur")
