"""
Définition des variables fixes de l'application
"""

from lxml import etree


xml = etree.parse("xml_tei/NDF_TEI.xml")

namespaces = {'tei':'http://www.tei-c.org/ns/1.0'}
xp_titres = "//tei:body/tei:div/tei:head/text()"
titres = xml.xpath(xp_titres, namespaces=namespaces)
