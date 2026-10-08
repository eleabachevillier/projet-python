from Document import Document

class RedditDocument(Document): # hérite de Animal
    def __init__(self, titre, auteur, date, url, texte,co_auteurs):
        super().__init__(titre, auteur, date, url, texte) # constructeur mère
        self.nb_commentaires=co_auteurs

    def getnb_commentaires(self):
        return f"le nombre de commentaires est {self.nb_commentaires}"
    
    def setnb_commentaires(self):
        set.nb_commentaires = nb_commentaires

    def crier(self): # surcharge (override)
        return f"{self.nom} aboie : Ouaf !"