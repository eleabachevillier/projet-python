from Document import Document

class RedditDocument(Document): # hérite de Animal
    def __init__(self, titre, auteur, date, url, texte,co_auteurs):
        super().__init__(titre, auteur, date, url, texte) # constructeur mère
        self.nb_commentaires=co_auteurs

    def getnb_commentaires(self):
        return self.nb_commentaires
    
    def setnb_commentaires(self):
        set.nb_commentaires = nb_commentaires

    def __str__(self): # surcharge (override)
         return f"[Reddit] {self.titre} - {self.nb_commentaires} commentaires"#mise en forme

    def getType(self):
        return "Reddit"