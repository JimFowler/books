<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text"/>
<xsl:template match="BookFile">
    <!-- deal with header -->
<xsl:for-each select="Header">
<xsl:value-of select="text()"/>
</xsl:for-each>
    
<xsl:for-each select="Entries/Entry">
\bkentry{<xsl:value-of select="Year"/>}
{<xsl:for-each select="Authors/Author">
<xsl:value-of select="Person/Last"/>, <xsl:value-of select="Person/First"/>
</xsl:for-each>}
{<xsl:value-of select="Title"/>}
{<xsl:for-each select="Publishers/Publisher">
<xsl:value-of select="Place"/>, <xsl:value-of select="Name"/>
</xsl:for-each>}
{}{}
<xsl:for-each select="Comments/Comment">
  <xsl:value-of select="text()"
/>
  
</xsl:for-each>

</xsl:for-each>

  </xsl:template>
</xsl:stylesheet>
