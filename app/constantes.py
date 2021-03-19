"""
Définition des variables constantes de l'application NDF
Author:Juliette Janes
Date: 03/03/2021
"""

# import de etree permettant de traiter les fichiers xml en python
from lxml import etree

# parsage du document TEI contenant les articles avec la mathode .parse() d'etree
document_xml = etree.parse("xml_tei/NDF_TEI.xml")

# parsage  de la feuille de transformation XSLT permettant la transformation du texte d'un article xml en html
affichage_texte = etree.parse("xml_tei/xslt_affichage_note.xsl")
# transformation du document xslt en objet xslt permettant de l'utiliser comme une fonction en python
xslt_transformation = etree.XSLT(affichage_texte)
