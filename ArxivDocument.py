from Document import Document

class RedditDocument(Document): # hérite de Animal
    def __init__(self, titre, auteur, date, url, texte,nb_commentaires):
        super().__init__(titre, auteur, date, url, texte) # constructeur mère
        self.nb_commentaires=nb_commentaires
   
   
    def crier(self): # surcharge (override)
        return f"{self.nom} aboie : Ouaf !"