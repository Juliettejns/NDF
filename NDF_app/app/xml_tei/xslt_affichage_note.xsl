<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
        
    <xsl:strip-space elements="*"/> <!-- pour éviter les espaces non voulus -->
       
    <xsl:param name="num"/>
    <xsl:variable name="note" select="descendant::text[@n=$num]"/>
     
    <xsl:template match="TEI">
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
    
    <xsl:template match="opener">
        <xsl:element name="div">
            <xsl:attribute name="align">
                <xsl:text>left</xsl:text>
            </xsl:attribute>
            <xsl:value-of select="dateline|quote"/>
        </xsl:element>
    </xsl:template>    
    <xsl:template match="closer">
        <xsl:element name="div">
            <xsl:attribute name="align">
                <xsl:text>right</xsl:text>
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
     <xsl:template match="div//p">
         <xsl:element name="p">
            <xsl:value-of select="."/>
         </xsl:element>
     </xsl:template>
    <xsl:template match="div//dateline">
        <xsl:element name="span">
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="quote">
        <xsl:element name="blockquote">
            <xsl:apply-templates select="p"/>
        </xsl:element>
    </xsl:template>
 
</xsl:stylesheet>