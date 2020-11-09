Description of AAA Data Files
*****************************

The AAA data files were obtained from ARIBib in 2009.
I had asked if I could troll through their database
and they responded that they already had the data files.

The books are generally in section 3 of AAA while the conference
proceedings are in section 12.  ??? sent both sections to me from all
73 volumes. The total number of book in these files is
13,157. However, I have noted the occasional book in other sections
that we not includes in these files. It will be necessary to search
through the volumes of AAA to locate these books.

The files are named aaaNNsSS.txt where NN is the volume number is SS
is the section number, either 03 or 12.  Each files contains a single
line per entry, with field names and field values separated by
a vertical bar, '|'.  An example is::

  |a|J._Blunck|t|Mars and its satellites.
  |s|J._Blunck. Exposition Press, Inc., Smithtown, N.Y. 11787-0817,
  USA. 222_pp. Price \partial _10.00 (1982).
  ISBN_0-682-49777-0._- Review in Sky Telesc., Vol._65, No._4, p._337 (1983).
  |k|Mars, Mars Satellites|n|AAA033.003.019

The known key fields are

  * a - authors or editors.  If editors, then the names are followed
    by ***(ed.)***, for a single editor or ***(eds.)***, if there are
    multiple editors. Multiple authors are editors are separated by a
    space character, but the names are terminated with a comma but the
    last author/editor does not have a comma, Under-bar '_' is used to
    separate first initial, middle initial, and last name.

  * t - Title of the book or proceedings.  The title is followed by a
    period so this will need to be removed. This field may contain multiple
    sub-titles and/or conference information.

  * y - copyright year.

  * k - keywords or topic separated by commas. Note that this field is
    not found in AJB. Will need to add a keyword field to the XML
    schema for bookfile. Keywords may have the form of a single word
    or phrase as well as phrase:phrase if there is a sub-topic. For
    example ***Hubble Constant:Supernovae*** or ***Galaxies:Distance
    Indicators***

  * n - the entry number of the form AAAvvv.sss.nnn, where vvv is
    the volume number, sss is the section number, and nnn is the entry
    number. Note that all volumes use per section counts for the entries.
    There are no sequential entry number for a single volumes as there are
    in the early volumes of AJB.

  * s - publishing information. Including place, publisher, pagination,
    and possibly other information. Place and publisher are separated
    by a colon. Reviews are also included here and may have different
    abbreviations than AJB.

  * j - the author/editor names are in ISO-8859-1 encoding. This field
    provides a 7-bit clean (ASCII) version of these names. Probably don't need
    to use this field.

  * m - this field was not described by ARIBib but it appears to be
    alternate spellings of author/editor names. This might be useful
    for searches. 

  * b - this field was not described by ARIBib but it is the ADS
    bibcode for the work. Appears to principally in conference
    proceedings, part 12.

  * l - this field was not described by ARIBib but is appears to be a
    coded link to the databases at the University of Chicago,
    Strausborg, or NAO in Japan.  Note that a number of conference
    proceedings appear to be journal publications rather than books.
    There is usually a link field in these entries and these journal
    publications need to be filtered out.

  * + - this field was not described by ARIBib but it appears to be a
    'see also' field. Possibly an addition to an entry or a previous
    edition of a work.
