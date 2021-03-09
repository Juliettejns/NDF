"""
Définition des variables fixes de l'application
"""

from lxml import etree


document_xml = etree.parse("xml_tei/NDF_TEI.xml")

affichage_texte = etree.parse("xml_tei/xslt_affichage_note.xsl")
xslt_transformation = etree.XSLT(affichage_texte)