﻿"""Parse a comment line from an AJB text file.  Separate
out the different sections of the comment.  The calling
function has to decide what to do with this information
but an example of how to get that information is included
in the unit test of this file.

Calling syntax:
    cParser = Comment.parser()
    result = cParser.parse_string( strComment )

See the test comments in the unit tests for an example
of how comments are written.
"""

import sys
from modgrammar import *
from modgrammar.extras import *

class Digit (Grammar):
    grammar = (WORD("0-9", count=1))
    grammar_collapse = True

class TwoDigit (Grammar):
    grammar = (WORD('0-9', count=2))
    grammar_collapse = True
    
class Year (Grammar):
    grammar = (WORD('0-9', count=4))

class Item (Grammar):
    grammar = (RE(r'[0-9]{2,3}'))

class Section (Grammar):
    grammar = (RE(r'[0-9]{2,3}'))

class Volume (Grammar):
    grammar = (TwoDigit)

class AJBNum (Grammar):
    grammar = (L('AJB'), Volume, '.', Section, '.', Item)

class uWord (Grammar):
    # one or more unicode characters.
    # also matches number and underscore.
    # Match a bunch of punctuation marks.
    # Punctuation marks are usually used in the Other grammar
    # but occasionally get used in the main entries.
    grammar=(RE(r"[-,!()<>?$£&.'′’/\w]+"))

class uAbrv (Grammar):
    # unicode possessive, (Was abreviation)
    # \u2019 is a right quote mark
    #grammar=(uWord, OR(LITERAL('.'), LITERAL('\u2019')))
    grammar=(uWord, LITERAL('\u2019'))

class uWord2 (Grammar):
    # unicode word or abbreviation
    grammar = (OR(uWord, uAbrv))

class uWord3 (Grammar):
    # hyphenated word or abbreviations
    grammar = (uWord2, OPTIONAL(WORD("&-"), uWord2))

class uWords (Grammar):
    """Many unicode words"""
    grammar = (REPEAT(uWord))

class Initial (Grammar):
    """Only capitalized initials are allowed"""
    grammar = (RE(r'\w'), LITERAL('.'))

class Name (Grammar):
    # accept hypenated first initial and hyphenated last name
    grammar = (OPTIONAL(Initial, OPTIONAL(L('-'), Initial)),
               OPTIONAL(REPEAT(Initial, OPTIONAL(L('-'), Initial))),
               uWords)

class NameList (Grammar):
    grammar = (LIST_OF(Name, sep='and'))

class FromLanguage(Grammar):
    grammar = (L('from'), uWord)

class ToLanguage(Grammar):
    grammar = (L('into'), uWord)

class Publisher (Grammar):
    """City: Name"""
    grammar = (uWords, L(':'), uWords)

class PublisherList (Grammar):
    grammar = (LIST_OF(Publisher, sep='and'))



#
# These are the main components of the Comment grammar.  Note that all
# phrases need to be terminated with a semi-colon except Reference
# otherwise the greedy function of the parser will keep waiting for
# more charactors and will not return the match. This is necessary for
# variable length grammars, like Editors, Translated, or Publisher
#

class Publishers (Grammar):
    grammar = (L('also published'), PublisherList, L(';'))

class Translation (Grammar):
    grammar = (L('translated'), OPTIONAL(FromLanguage),
               OPTIONAL(ToLanguage), OPTIONAL(L('by'), NameList), L(';'))

class Editors (Grammar):
    grammar = (L('edited by'), NameList, L(';'))

class Compilers (Grammar):
    grammar = (L('compiled by'), NameList, L(';'))

class Contributors (Grammar):
    grammar = (L('contributors'), NameList, L(';'))

class Reprint (Grammar):
    grammar = (L('reprint of'), OR(AJBNum, Year), L(';'))

class Reference (Grammar):
    grammar = (L('reference'), AJBNum)
  
class Edition (Grammar):
    grammar = (OR(Digit, TwoDigit),
               OR(L('nd'), L('rd'), L('st'), L('th')),
               OPTIONAL(OR(L('facsimile'), L('revised'))), L('edition'), L(';'))

    def elem_init(self, sessiondata):
        self.edition_num = self[0].string

class LanguageList (Grammar):
    grammar = (LIST_OF(uWords, sep='and'))

class Language (Grammar):
    grammar = (L('in'), LanguageList,
               OPTIONAL( L('with'), uWords, L('references')),  L(';'))

class Other (Grammar):
    """match string with any unicode character except whitespace
    and a semi-colon"""
    #grammar = (L('other'), REPEAT(RE(r"[0-9()?'\w]+")), L(';'))
    grammar = (L('other'), uWords, L(';'))

class Comment (Grammar):
    grammar = (OR(Edition, Compilers, Contributors, 
                  Reference, Reprint, 
                  Editors, Translation, Publishers,
                  Language, Other))


if __name__ == '__main__':

    teststr = ['2nd edition;',
               '3rd edition;',
               '7th revised edition;',
               '17th revised edition;',
               
               'reprint of 1956;',
               'reprint of AJB 34.56.23;',
               
               'reference AJB 66.54.32 ',
    
               'edited by A. J. Reader;',
               'edited by A.-B. J. Reader;',
               'edited by A. B. J. Reader;',
               'edited by A.-B. C.-D. J. Reader;',
               'edited by A. Reader and I. M. Writer;',

               'compiled by A. J. Reader;',
               'compiled by A.-B. J. Reader;',
               'compiled by A. Reader and I. M. Writer;',

               'contributors A. J. Reader;',
               'contributors A.-B. J. Reader;',
               'contributors A. Reader and I. M. Writer;',

               'translated by A. J. Reader-Writer; ',
               'translated by A. Reader; ',
               'translated by A. Reader and I. M. Writer; ',
               'translated from Italian; ',
               'translated into French; ',
               'translated from Italian into French; ',
               'translated from Italian by A. J. Reader; ',
               'translated from Italian into French by A. J. Reader; ',
               'translated from Italian into French by A. J. Reader and I. M. Writer; ',

               'in Italian;',
               'in French and Italian;',
               'in French with Russian references; ',

               'also published London: Big City Publisher; ',
               'also published London: Rand McNally & Sons; ',
               "also published London: St. Martin\u2019s Press;",
               # a unicode city for when we figure out unicode words
               'also published G\u00F6ttingen: Big City Publisher; ',
               'also published New York: Another Big City Publisher Ltd.; ',
               'also published New York: Another Big City, Publisher Ltd. and London: Phys.-Math. Staatsverlag; ',

               'other now is the time for all good men ;',
               'other <<The Books at Large>>;',
               'other you should be able to write anything here including (45) _ and Abrvs.;']

    fullstr = 'other extraneous material that I do not yet know how to handle; also published New York: Another Big City Publisher Ltd. and London: Big City Publisher; translated from Italian into French by A. J. Trans and I. M. Trans; edited by A. Reader and I. M. Writer; reprint of AJB 34.56.23; 7th revised edition; in Russian;'

    cParser = Comment.parser()
    count = 0

    for comment in teststr:
        print('\nComment is ', comment)
        result = cParser.parse_string(comment)
        if result:
            grmName = result.elements[0].grammar_name
            print(grmName)
            print(result)
        else:
            print('bad result!')
            print(type(comment))
            count += 1
        cParser.reset()

    print( '\nDoing full string')
    result = cParser.parse_string(fullstr, reset=True)
    if not result:
        print('bad result for')
        print(fullstr)
        count += 1
    while result:
        grmName = result.elements[0].grammar_name
        print('\n'+grmName)
        if 'Edition' ==  grmName:
            tmp = result.elements[0].edition_num
            print(tmp)

        elif 'Reference' == grmName:
            tmp = result.find(AJBNum)
            print(str(tmp))

        elif 'Reprint' == grmName:
            tmp = result.find(AJBNum)
            if tmp:
                print('AJBNum is ' + str(tmp))
            tmp = result.find(Year)
            if tmp:
                print('Year is ' + str(tmp))

        elif 'Editors' == grmName:
            tmp = result.find(NameList)
            # parse the NameList
            print(str(tmp))

        elif 'Compilers' == grmName:
            tmp = result.find(NameList)
            # parse the NameList
            print(str(tmp))

        elif 'Contributors' == grmName:
            tmp = result.find(NameList)
            # parse the NameList
            print(str(tmp))

        elif 'Translation' == grmName :
            tmp = result.find(FromLanguage)
            if tmp:
                print(tmp.elements[1])
            tmp = result.find(ToLanguage)
            if tmp:
                print(tmp.elements[1])
            tmp = result.find(NameList)
            if tmp:
                # parse the NameList
                print(str(tmp))

        elif 'Publishers' == grmName:
            tmp = result.find(PublisherList)
            # parse the PublisherList
            print(tmp)

        elif 'Language' == grmName:
            tmp = result.find(uWord)
            # get the language
            print(tmp)

        elif 'Other' == grmName:
            tmp = result.find(uWords)
            # parse the PublisherList
            print(tmp)

        result = cParser.parse_string('')

    print('\n')
    sys.stdout.writelines(generate_ebnf(Comment))

    """
    nm = FromLanguage.parser()
    result = nm.parse_string( 'from Italian ' )
    print( result.elements )
    """
    if 1 == count:
        s = ' '
    else:
        s = 's'
    result = '\nDone! %d error%c' % (count, s)
    print(result)

