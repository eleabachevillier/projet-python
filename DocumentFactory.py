from Document import Document
from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument

class Fabrique:
    def document_factory(source, titre, auteur, date, url, texte, **kwargs): #autres paramentres, avec nb variable
        if source.lower() == "reddit":
            return RedditDocument(
                titre, auteur, date, url, texte,
                kwargs.get("nb_commentaires", 0)
            )
        elif source.lower() == "arxiv":
            return ArxivDocument(
                titre, auteur, date, url, texte,
                kwargs.get("coauteurs", [])
            )
        else:
            raise ValueError("Source inconnue")