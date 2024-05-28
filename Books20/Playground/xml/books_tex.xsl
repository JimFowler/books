<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text"/>
  <xsl:template match="BookFile">
    <xsl:value-of select="Header"/>
    <xsl:for-each select="Entries/Entry">
\bkentry{<xsl:value-of select="Year"/>}{The Author}
{<xsl:value-of select="Title"/>}
{Place, Publisher}
{<xsl:value-of select="Pagination"/>}
{<xsl:value-of select="Index/IndexName"/> <xsl:value-of select="Index/VolumeNumber"/>.<xsl:value-of select="Index/SectionNumber"/>(<xsl:value-of select="Index/SubSectionNumber"/>).<xsl:value-of select="Index/EntryNumber"/>}
<xsl:value-of select="Comments"/>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>

<!-- Begin copyright

  /home/jrf/Documents/books/Books20/Tools/xml/books_tex.xsl

   Part of the Books20 Project

   Copyright 2019 James R. Fowler

   All rights reserved. No part of this publication may be
   reproduced, stored in a retrival system, or transmitted
   in any form or by any means, electronic, mechanical,
   photocopying, recording, or otherwise, without prior written
   permission of the author.


End copyright -->


