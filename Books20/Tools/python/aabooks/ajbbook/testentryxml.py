#! /usr/bin/env python
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/testentryxml.py
##
##   Part of the Books20 Project
##
##   Copyright 2020 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright
'''The file contains the test set of xml descriptions of various
AJBentry types as defined in ajbentry.py.  These descriptions are
used in testing entryxml.py and AJBentry.py.
'''

ENTRY_XML_STR = '''<Entry>
  <Index>
    <IndexName>AJB</IndexName>
    <VolumeNumber>66</VolumeNumber>
    <SectionNumber>145</SectionNumber>
    <SubSectionNumber>0</SubSectionNumber>
    <EntryNumber>29a</EntryNumber>
    <PageNumber>24</PageNumber>
  </Index>
  <Title>The Physics, and Astronomy of Galaxies and Cosmology</Title>
  <Authors>
    <Author>
      <Person>
        <First>P.</First>
        <Middle>W.</Middle>
        <Last>Hodge</Last>
        <Suffix>jr.</Suffix>
      </Person>
    </Author>
    <Author>
      <Person>
        <First>I.</First>
        <Middle>A. Author</Middle>
        <Last>Other</Last>
      </Person>
    </Author>
    <Author>
      <Person>
        <First>A.</First>
        <Middle>V.</Middle>
        <Last>de la Name</Last>
      </Person>
    </Author>
  </Authors>
  <Editors>
    <Editor>
      <Person>
        <First>A.</First>
        <Middle>B.</Middle>
        <Last>Name</Last>
      </Person>
    </Editor>
  </Editors>
  <Publishers>
    <Publisher>
      <Place>New York</Place>
      <Name>McGraw-Hill Book Company</Name>
    </Publisher>
    <Publisher>
      <Place>Londön</Place>
      <Name>A Publishing Co.</Name>
    </Publisher>
  </Publishers>
  <Year>1966</Year>
  <Edition>3</Edition>
  <Pagination>179 pp</Pagination>
  <Prices>
    <Price>$2.95</Price>
    <Price>$4.95</Price>
  </Prices>
  <Reviews>
    <Review>Sci. American 216 Nr 2 142</Review>
    <Review>Sky Tel. 33 164</Review>
  </Reviews>
  <TranslatedFrom>Itälian</TranslatedFrom>
  <Language>French</Language>
  <Translators>
    <Translator>
      <Person>
        <First>A.</First>
        <Last>Trans</Last>
      </Person>
    </Translator>
  </Translators>
  <TranslationOf>
    <Index>
      <IndexName>AJB</IndexName>
      <VolumeNumber>47</VolumeNumber>
      <SectionNumber>144</SectionNumber>
      <SubSectionNumber>0</SubSectionNumber>
      <EntryNumber>23a</EntryNumber>
    </Index>
  </TranslationOf>
  <Compilers>
    <Compiler>
      <Person>
        <First>A.</First>
        <Middle>B.</Middle>
        <Last>Compiler</Last>
      </Person>
    </Compiler>
  </Compilers>
  <Contributors>
    <Contributor>
      <Person>
        <First>A.</First>
        <Middle>B.</Middle>
        <Last>Contrib</Last>
      </Person>
    </Contributor>
  </Contributors>
  <ReprintOf>
    <Year>1956</Year>
  </ReprintOf>
  <ReferenceOf>
    <Index>
      <IndexName>AJB</IndexName>
      <VolumeNumber>59</VolumeNumber>
      <SectionNumber>144</SectionNumber>
      <SubSectionNumber>0</SubSectionNumber>
      <EntryNumber>55b</EntryNumber>
    </Index>
  </ReferenceOf>
  <Comments>
    <Comment>a first comment</Comment>
    <Comment>This is the editor string</Comment>
  </Comments>
</Entry>
'''
