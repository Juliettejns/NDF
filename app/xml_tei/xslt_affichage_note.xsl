<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
        
    <xsl:strip-space elements="*"/> <!-- pour éviter les espaces non voulus -->
    
    <!--définition des différents paramètres possibles à ajouter depuis routes.py-->
    <!--identifiant permettant de sélectionner l'article voulu-->
    <xsl:param name="num"/>
    <!--pointeur pour surligner un élément (lieu ou personne) dans la route surlignage-->
    <xsl:param name="pointeur"/>
 
    
    <!--récupération de l'article choisi-->
    <xsl:variable name="note" select="descendant::text[@n=$num]"/>
     
     <!--construction de la structure html-->
    <xsl:template match="TEI">
        <br/>
        <xsl:element name="span">
            <xsl:element name="a">
                <xsl:attribute name="href">
                    <xsl:value-of select="$note/@facs"/>
                </xsl:attribute>
                <xsl:text>Lien</xsl:text>
            </xsl:element>
            <xsl:text> vers le journal numérisé sur Gallica</xsl:text>
        </xsl:element>
        <br/>
        <xsl:apply-templates select="$note//div"/>
    </xsl:template>
    
    <!--structuration des éléments autour des paragraphes (opener, closer, postcript et quote)-->
    <xsl:template match="opener">
        <xsl:element name="div">
            <xsl:attribute name="align">
                <xsl:text>right</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="dateline|quote"/>
        </xsl:element>
    </xsl:template>    
    <xsl:template match="closer">
        <xsl:element name="div">
            <xsl:attribute name="align">
                <xsl:text>center</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="postscript">
        <xsl:element name="div">
            <xsl:attribute name="align">
                <xsl:text>left</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates select="p"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="cit">
        <xsl:element name="div">
            <xsl:attribute name="align">
                <xsl:text>left</xsl:text>
            </xsl:attribute>
        <xsl:apply-templates select="quote"/>
        <xsl:element name="cite">
            <xsl:attribute name="align">
                <xsl:text>right</xsl:text>
            </xsl:attribute>
             <xsl:value-of select="ref"/>
        </xsl:element>
        </xsl:element>
    </xsl:template>
    <xsl:template match="quote">
        <xsl:element name="blockquote">
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

<!--structuration de la dateline-->
    <xsl:template match="div//dateline">
        <xsl:element name="span">
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
    <!--structuration des paragraphes avec des alinéas-->
     <xsl:template match="div//p">
         <xsl:element name="p">
            <xsl:text>&#160; &#160;</xsl:text>
             <xsl:apply-templates select="node()"/>
         </xsl:element>
     </xsl:template>
    <!--structuration des éléments à l'intérieur des paragraphes
        on les intègre grâce à select node() qui permet de sélectionner le noeud
        sur lequel on a match-->
    <xsl:template match="hi">
        <xsl:element name="i">
            <xsl:apply-templates select="node()"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="persName">
        <xsl:choose>
            <xsl:when test="translate(@ref,'#','')=$pointeur">
                <xsl:element name="span">
                    <xsl:attribute name="style">
                        <xsl:text>background-color:red</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates select="node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="node()"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="placeName">
          <xsl:choose>
            <xsl:when test="translate(@ref,'#','')=$pointeur">
                <xsl:element name="span">
                    <xsl:attribute name="style">
                        <xsl:text>background-color:red</xsl:text>
                    </xsl:attribute>
                    <xsl:apply-templates select="node()"/>
                </xsl:element>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="node()"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>    

</xsl:stylesheet>
