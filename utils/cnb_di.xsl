<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns="http://www.loc.gov/MARC21/slim"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

<xsl:output method="xml" indent="yes" />

<xsl:template match="/">
<collection>
<xsl:for-each select=".//marc:record">
<record>
    <SYSNO><xsl:value-of select=".//*[@tag='001']/text()" /></SYSNO>
    <title>
        <xsl:value-of select=".//*[@tag='245']/*[@code='a']/text()" /><xsl:value-of select="' '"/>
        <xsl:value-of select=".//*[@tag='245']/*[@code='n']/text()" /><xsl:value-of select="' '"/>
        <xsl:value-of select=".//*[@tag='245']/*[@code='p']/text()" />
    </title>
    <key-title><xsl:value-of select=".//*[@tag='222']/*[@code='a']/text()" /></key-title>
    <author><xsl:value-of select=".//*[@tag='100' and ./*[@code='4']/text()='aut']/*[@code='a']/text()"/></author>
    <!-- <language><xsl:value-of select = ".//*[@tag='041']/*[@code='a']/text()"/></language> -->
    <ISBN><xsl:value-of select=".//*[@tag='020']/*[@code='a']/text()" /></ISBN>
    <ISSN><xsl:value-of select=".//*[@tag='022']/*[@code='a']/text()" /></ISSN>
    <ccnb><xsl:value-of select=".//*[@tag='015']/*/text()" /></ccnb>
    <link><xsl:value-of select="normalize-space(.//*[@tag='856' and @ind1='4' and @ind2='1']/*[@code='u']/text())" /></link>
</record>
</xsl:for-each>
</collection>
</xsl:template>

<xsl:template match="*" mode="remove-namespace">
    <xsl:element name="{local-name()}">
        <xsl:copy-of select="@*" />
        <xsl:apply-templates select="node()" mode="remove-namespace"/>
    </xsl:element>
</xsl:template>

<xsl:template match="datafield/text()" mode="remove-namespace">
    <xsl:value-of select="normalize-space()"/>
</xsl:template>

</xsl:stylesheet>