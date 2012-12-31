Classes
*******

Basic Classes
-------------

BookEntry
_________

.. automodule:: BookEntry
    :members:
    :show-inheritance:

Entry
_____

.. automodule:: entry
    :members:
    :show-inheritance:

AJB Comments
____________


AJB entries have much common information however there are entries
that have additional information that is not common enough to have an
additional field in the Book Entry. For this additional information
there is a comment field defined. The comment infomation does have
enough common features that we have defined a grammer to allow for
automatic parsing of the field but have also allowed a grammer that allow
one to put anything in the field.  The grammer is defined as:

.. productionlist:: AJBcomments
  Comment       : ( Edition | Compilers | Contributors | Reference | Reprint |
                : Editors | Translation | Publishers | Language | Other );
  Edition       : ( Digit | TwoDigit ), ( 'nd' | 'rd' | 'st' | 'th' ), [(
                : 'facsimile' | 'revised' )], 'edition', ';';
  Compilers     : 'compiled by', NameList, ';';
  Contributors  : 'contributors', NameList, ';';
  Reference     : 'reference', AJBNum;
  Reprint       : 'reprint of', ( AJBNum | Year ), ';';
  Editors       : 'edited by', NameList, ';';
  Translation   : 'translated', [FromLanguage], [ToLanguage], ['by', NameList], ';';
  Publishers    : 'also published', PublisherList, ';';
  Language      : 'in', LanguageList, ['with', uWords, 'references'], ';';
  Other         : 'other', uWords, ';';
  Digit         : ? WORD('0-9') ?;
  TwoDigit      : ? WORD('0-9') ?;
  NameList      : Name, {Name};
  AJBNum        : 'AJB', Volume, '.', Section, '.', Item;
  Year          : ? WORD('0-9') ?;
  FromLanguage  : 'from', uWord;
  ToLanguage    : 'into', uWord;
  PublisherList : Publisher, {Publisher};
  LanguageList  : uWords, {uWords};
  uWords        : uWord, {uWord};
  Name          : [Initial, ['-', Initial]], [( Initial, ['-', Initial] ),
                : {Initial, ['-', Initial]}], uWords;
  Volume        : TwoDigit;
  Section       : ? <RE> ?;
  Item          : ? <RE> ?;
  uWord         : ? <RE> ?;
  Publisher     : uWords, ':', uWords;
  Initial       : ? <RE> ?, '.';


.. automodule:: AJBcomments
    :members:
    :show-inheritance:

