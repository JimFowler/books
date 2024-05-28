<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="text"/>
<xsl:template match="system">

#include "<xsl:value-of select="@name"/>_handler_doc.h"

<xsl:for-each select="handler">

MessageHandlerDescriptor <xsl:value-of select="@name"/>_descriptor
(
"<xsl:value-of select="normalize-space(@name)"/>",
"<xsl:value-of select="normalize-space(../@name)"/>",
"<xsl:value-of select="normalize-space(text())"/>",
_REVISION,
<xsl:value-of select="@reentrant"/>
);

</xsl:for-each>


void initialize_handlers()
{

<xsl:for-each select="handler">

<xsl:for-each select="required_parm">
  <xsl:value-of select="../@name"/>_descriptor.add_required_parm( "<xsl:value-of select="normalize-space(@name)"/>",
  "<xsl:value-of select="@type"/>",
  "<xsl:value-of select="normalize-space(text())"/><xsl:if test="@unit != ''"> (<xsl:value-of select="@unit"/>)</xsl:if>" );
</xsl:for-each>


<xsl:for-each select="optional_parm">
  <xsl:value-of select="../@name"/>_descriptor.add_optional_parm( "<xsl:value-of select="normalize-space(@name)"/>",
  "<xsl:value-of select="@type"/>",
  "<xsl:value-of select="normalize-space(text())"/><xsl:if test="@unit != ''"> (<xsl:value-of select="@unit"/>)</xsl:if>" );
</xsl:for-each>

</xsl:for-each>

}

</xsl:template>
</xsl:stylesheet>
