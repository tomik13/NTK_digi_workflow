<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    xmlns="http://www.loc.gov/MARC21/slim"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    >

<xsl:output method="xml" indent="yes" />

<xsl:param name="FMT"/>

<xsl:template match="/">
<collection>
<xsl:for-each select=".//marc:record">
    <xsl:apply-templates select="." mode="remove-namespace"/>    
    </xsl:for-each>
</collection>
</xsl:template>

<xsl:template match="*" mode="remove-namespace">
    <xsl:element name="{local-name()}">
        <xsl:copy-of select="@*" />
        <xsl:apply-templates select="node()" mode="remove-namespace"/>
    </xsl:element>
</xsl:template>

<xsl:template match="marc:datafield/text()" mode="remove-namespace">
    <xsl:value-of select="normalize-space()"/>
</xsl:template>

</xsl:stylesheet>