from Document import Document

class ArxivDocument(Document): # hérite de Animal
    def __init__(self, titre, auteur, date, url, texte,coauteurs):
        super().__init__(titre, auteur, date, url, texte) # constructeur mère
        self.coauteurs=coauteurs
   
   
    #surcharge (override)
    def getCoauteurs(self):
        return self.coauteurs

    def setCoauteurs(self, coauteurs):
        self.coauteurs = coauteurs

    def __str__(self):
        return f"[Arxiv] {self.titre} - {len(self.coauteurs)} coauteurs"#coauteurs : liste
    
    def getType(self):
        return "Arxiv"