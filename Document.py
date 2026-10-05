class Document :
    """document reddit et arxiv"""
    """il faudra mettre les arguments en pv"""

    def __init__ (self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date=date
        self.url=url
        self.texte=texte

    def __str__(self):
        return f"le titre du document est : {self.titre} et l'auteur est : {self.auteur}, enfin le texte est : {self.texte} et la date est : {self.date} et l'url est : {self.url}"



