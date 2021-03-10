<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
    <xsl:output method="html" indent="yes" encoding="UTF-8"/>
    
    <xsl:strip-space elements="*"/> <!-- pour éviter les espaces non voulus -->
    
    <xsl:param name="num"/>
    <xsl:variable name="note" select="descendant::text[@n=$num]"/>
    
    <xsl:template match="/">
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
    
    <xsl:template match="div">
        <xsl:choose>
            <xsl:when test="dateline">
                <xsl:apply-templates select="dateline"/>
            </xsl:when>
        </xsl:choose>
        <xsl:element name="div">
            <xsl:apply-templates select="p|quote"/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="div/dateline">
        <xsl:element name="span">
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="div/p">
        <xsl:element name="p">
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>
    
    <xsl:template match="quote">
        <xsl:element name="p">
            <xsl:element name="i">
                <xsl:value-of select="."/>
            </xsl:element>
        </xsl:element>
    </xsl:template>
    

</xsl:stylesheet>