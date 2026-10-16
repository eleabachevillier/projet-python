txt = "welcome to the jungle"

x = txt.split()

print(x)


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
            valeurs.append(compteur[mot])

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



requete = input("Que recherchez-vous ? ")
mots_rq = corp_champ.nettoyer_texte(requete).split()

mots_presents = {mot: i for i, mot in enumerate(mots_vocab)}#dictionnaire des mots avec id
#vocab = dict(vocab.items())

# Construire le vecteur TF de la requête
vecteur = np.zeros(len(mots_vocab))#tableau de 0 de taille mot_vocab
for mot in mots_rq:
    if mot in mots_presents:
        vecteur[mots_presents[mot]] += 1

# Appliquer les poids IDF
#vecteur = vecteur * freq["idf"].to_numpy()              #PAS FREQ IDF JE VEUX MULTIPLIER AVEC DONNEES DE LA MATRICE IDF
#vecteur = vecteur @ mat_TF        #term frequency       #voir si peut faire avec la matrice
vecteur = vecteur * freq["idf"].to_numpy()

# Calculer les cosinus avec chaque document
produits = mat_TFxIDF @ vecteur
#IA
normes_docs = np.sqrt(np.asarray(mat_TFxIDF.multiply(mat_TFxIDF).sum(axis=1)).ravel())
norme_requete = np.linalg.norm(vecteur)
print ("\n\n\n norme requete :", norme_requete)

scores = np.zeros(len(produits))#tab 0 de taille tf idf+vecteur(mots, 1)

if norme_requete != 0:
    denominateurs = normes_docs * norme_requete
    scores = np.divide(
        produits.ravel(),
        denominateurs,
        out=np.zeros_like(normes_docs, dtype=float),
        where=denominateurs != 0
    )

    
#fin IA 
"""