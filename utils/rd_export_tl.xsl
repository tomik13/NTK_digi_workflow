<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:marc="http://www.loc.gov/MARC21/slim"
    xmlns="http://www.loc.gov/MARC21/slim"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

<xsl:output method="xml" indent="yes" />

<xsl:param name="FMT"/>
<xsl:param name="recId"/>

<xsl:template match="/">
<xsl:for-each select=".//marc:record">
    <record
    xmlns="http://www.loc.gov/MARC21/slim"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <xsl:for-each select="./*">
            <xsl:choose>

                <xsl:when test="@tag = '001'">
                    <controlfield tag="FMT">
                        <xsl:value-of select="$FMT" />
                    </controlfield>
                    <!-- <xsl:apply-templates select="." mode="remove-namespace"/> -->
                    <controlfield tag="001">
                        <xsl:value-of select="$recId" />
                    </controlfield>
                </xsl:when>

                <xsl:when test="starts-with(@tag,'99')" />

                <xsl:when test="@tag = 856 and not(starts-with(./*[@code = 'u']/text(), 'https://kramerius.techlib'))" />

                <xsl:otherwise>
                    <xsl:apply-templates select="." mode="remove-namespace" />
                </xsl:otherwise>

            </xsl:choose>
        </xsl:for-each>
    </record>      
</xsl:for-each>
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