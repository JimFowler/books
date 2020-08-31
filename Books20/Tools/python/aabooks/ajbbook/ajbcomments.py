## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Tools/python/aabooks/ajbbook/ajbcomments.py
##
##   Part of the Books20 Project
##
##   Copyright 2018 James R. Fowler
##
##   All rights reserved. No part of this publication may be
##   reproduced, stored in a retrival system, or transmitted
##   in any form or by any means, electronic, mechanical,
##   photocopying, recording, or otherwise, without prior written
##   permission of the author.
##
##
## End copyright

"""Parse a comment line from an AJB text file.  Separate
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

import modgrammar as mg
import modgrammar.extras as mge

mg.grammar_whitespace_mode = 'optional'

class WhiteSpace(mg.Grammar):
    '''Parse white space.'''
    grammar = (mge.RE(r'[ \t\r\n]+'))

class Digit(mg.Grammar):
    '''Parse single digit number.'''
    grammar = (mg.WORD("0-9", count=1))
    grammar_collapse = True

class TwoDigit(mg.Grammar):
    '''Parse a two digit number.'''
    grammar = (mg.WORD('0-9', count=2))
    grammar_collapse = True

class Year(mg.Grammar):
    '''parse a 4 digit year.'''
    grammar = (mg.WORD('0-9', count=4))

class Item(mg.Grammar):
    '''Parse the item (entry) number.'''
    grammar = (mge.RE(r'[0-9]{2,3}[a-c]*'))

# Note that no subsection is needed

class Section(mg.Grammar):
    '''Parse a section number.'''
    grammar = (mge.RE(r'[0-9]{2,3}'))

class Volume(mg.Grammar):
    '''Parse the volume number.'''
    grammar = (TwoDigit)

class AJBNum(mg.Grammar):
    '''Parse an AJB number.'''
    grammar = (mg.L('AJB'), Volume, '.', Section, '.', Item)

class Word(mg.Grammar):
    '''one or more unicode characters.'''
    # also matches number and underscore.
    # Match a bunch of punctuation marks.
    # Punctuation marks are usually used in the Other grammar
    # but occasionally get used in the main entries.
    grammar = (mge.RE(r"[-,!()+<>?$£&.°'′’/\w]+"))

class Abrv(mg.Grammar):
    '''unicode possessive, (Was abreviation)'''
    # \u2019 is a right quote mark
    #grammar=(Word, OR(LITERAL('.'), LITERAL('\u2019')))
    grammar = (Word, mg.LITERAL('\u2019'))

class Word2(mg.Grammar):
    '''unicode word or abbreviation'''
    grammar = (mg.OR(Word, Abrv))

class Word3(mg.Grammar):
    '''A word with & and - included.'''
    # hyphenated word or abbreviations
    grammar = (Word2, mg.OPTIONAL(mg.WORD("&-"), Word2))

class Words(mg.Grammar):
    '''Many unicode words'''
    grammar = (mg.REPEAT(Word))

class Initial(mg.Grammar):
    '''Only capitalized initials are allowed'''
    grammar = (mge.RE(r'\w'), mg.LITERAL('.'))

class Name(mg.Grammar):
    '''Parse a name from a comment.'''
    # accept hypenated first initial and hyphenated last name
    grammar = (mg.OPTIONAL(Initial, mg.OPTIONAL(mg.L('-'), Initial)),
               mg.OPTIONAL(mg.REPEAT(Initial, mg.OPTIONAL(mg.L('-'), Initial))),
               Words)

class NameList(mg.Grammar):
    '''Parse a namelist in a comment.'''
    grammar = (mg.LIST_OF(Name, sep='and'))

class FromLanguage(mg.Grammar):
    '''Parse a from language comment.'''
    grammar = (mg.L('from'), Word)

class ToLanguage(mg.Grammar):
    '''Parse a to language comment.'''
    grammar = (mg.L('into'), Word)

class Publisher(mg.Grammar):
    '''Parse a publisher comment of the form City: Name'''
    grammar = (Words, mg.L(':'), Words)

class PublisherList(mg.Grammar):
    '''Parse a publishers list comment.'''
    grammar = (mg.LIST_OF(Publisher, sep='and'))



#
# These are the main components of the Comment grammar.  Note that all
# phrases need to be terminated with a semi-colon except Reference
# otherwise the greedy function of the parser will keep waiting for
# more charactors and will not return the match. This is necessary for
# variable length grammars, like Editors, Translated, or Publisher
#

class Publishers(mg.Grammar):
    '''Parse a publisher comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('also published'), PublisherList,
               mg.L(';'))

class Translation(mg.Grammar):
    '''Parse a translation comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('translated'), mg.OPTIONAL(FromLanguage),
               mg.OPTIONAL(ToLanguage), mg.OPTIONAL(mg.L('by'), NameList),
               mg.L(';'))

class Editors(mg.Grammar):
    '''Parse an editors comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('edited by'), NameList,
               mg.L(';'))

class Compilers(mg.Grammar):
    '''Parse a compilers comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('compiled by'), NameList,
               mg.L(';'))

class Contributors(mg.Grammar):
    '''Parse a contributors comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('contributors'), NameList,
               mg.L(';'))

class Reprint(mg.Grammar):
    '''Parse a reprint comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('reprint of'), mg.OR(AJBNum, Year),
               mg.L(';'))

class Reference(mg.Grammar):
    '''Parse a reference comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('reference'), AJBNum,
               mg.L(';'))

class Edition(mg.Grammar):
    '''Parse an edition comment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.OR(Digit, TwoDigit),
               mg.OR(mg.L('nd'), mg.L('rd'), mg.L('st'), mg.L('th')),
               mg.OPTIONAL(mg.OR(mg.L('facsimile'), mg.L('revised'))), mg.L('edition'),
               mg.L(';'))

    def grammar_elem_init(self, sessiondata):
        '''initialize the element.'''
        self.edition_num = self[1].string
        
class LanguageList(mg.Grammar):
    '''Parse a language list comment.'''
    grammar = (mg.LIST_OF(Words, sep='and'))

class Language(mg.Grammar):
    '''Parse a language comment'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('in'), LanguageList,
               mg.OPTIONAL(mg.L('with'), Words, mg.L('references')),
               mg.L(';'))

class Other(mg.Grammar):
    '''Parse an 'other' commment.'''
    grammar = (mg.OPTIONAL(WhiteSpace),
               mg.L('other'), Words,
               mg.L(';'))

class Comment(mg.Grammar):
    '''Parse a comment string.'''
    grammar = (mg.OR(Edition, Compilers, Contributors,
                     Reference, Reprint,
                     Editors, Translation, Publishers,
                     Language, Other))


if __name__ == '__main__':

    import sys
    import unittest

    def write_ebnf_form():
        '''Write out the Extended Baccus-Naur form.'''
        sys.stdout.writelines(mg.generate_ebnf(Comment))

    class AjbCommentTestCase(unittest.TestCase):
        '''Define tests for the AJBComment functions.'''

        def setUp(self):
            '''Set up a parser for each test.'''
            self.comment_parser = Comment.parser()

        def tearDown(self):
            '''Clean up our mess after each test.'''
            del self.comment_parser

        def test_a_comments(self):
            '''Test individual comments. Really should test each comment
            for an expected result rather than any result.'''
            count = 0
            for comment in TESTSTR:
                result = self.comment_parser.parse_string(comment)
                if not result:
                    count += 1
            self.comment_parser.reset()

            self.assertEqual(count, 0)

        def test_b_full_string(self):
            '''Test a full string of comments.'''
            result = self.comment_parser.parse_text(FULLSTR,
                                                    reset=True, multi=True)
            self.assertTrue(result, msg='full string parse failed')

    # This should be a set of tuples with the comment, a result, and a
    # function that returns the proper result to compare with.
    TESTSTR = ['  2nd edition;',
               '3rd edition;',
               '7th revised edition;',
               '17th revised edition;',

               'reprint of 1956;',
               'reprint of AJB 34.56.23;',

               'reference AJB 66.54.32;',
               'reference AJB 66.54.32a;',
               'reference AJB 66.54.32c;',
               'reference AJB 66.54.32;',

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

               'translated by A. J. Reader-Writer;',
               'translated by A. Reader;',
               'translated by A. Reader and I. M. Writer;',
               'translated from Italian;',
               'translated into French;',
               ' translated from Italian into French;',
               'translated from Italian by A. J. Reader;',
               'translated from Italian into French by A. J. Reader;',
               'translated from Italian into French by A. J. Reader and I. M. Writer;',

               'in Italian;',
               'in French and Italian;',
               'in French with Russian references;',

               ' also published London: Big City Publisher;',
               'also published London: Rand McNally & Sons;',
               "also published London: St. Martin\u2019s Press;",
               # a unicode city for when we figure out unicode words
               'also published G\u00F6ttingen: Big City Publisher;',
               'also published New York: Another Big City Publisher Ltd.;',
               ''' also published New York: Another Big City, Publisher Ltd. \
and London: Phys.-Math. Staatsverlag;''',

               'other now is the time for all good men ;',
               'other <<The Books at Large>>;',
               '''other you should be able to write anything here including \
(45) _ and Abrvs.;''']

    FULLSTR = '''other extraneous material that I do not yet know how to \
handle; also published New York: Another Big City Publisher Ltd. and London: \
Big City Publisher; translated from Italian into French by A. J. Trans and I. \
M. Trans; edited by A. Reader and I. M. Writer; reprint of AJB 34.56.23; 7th \
revised edition; in Russian;'''

    NEWFULLSTR = '''other extraneous material that I do not yet know how to \
handle; translated from Italian into French by A. J. Trans and I. M. Trans; \
edited by A. Reader and I. M. Writer; reprint of AJB 34.56.23; 7th revised \
edition; in Russian;'''

    unittest.main()


UNUSED = '''
    def print_result(result):
        """Print the results after parsing the comments."""
        grm_name = result.elements[0].grammar_name
        print(grm_name)

        if grm_name == 'Edition':
            tmp = result.elements[0].edition_num
            print(tmp)

        elif grm_name == 'Reference':
            tmp = result.find(AJBNum)
            print(str(tmp))

        elif grm_name == 'Reprint':
            tmp = result.find(AJBNum)
            if tmp:
                print('AJBNum is ' + str(tmp))
            tmp = result.find(Year)
            if tmp:
                print('Year is ' + str(tmp))

        elif grm_name == 'Editors':
            tmp = result.find(NameList)
            # parse the NameList
            print(str(tmp))

        elif grm_name == 'Compilers':
            tmp = result.find(NameList)
            # parse the NameList
            print(str(tmp))

        elif grm_name == 'Contributors':
            tmp = result.find(NameList)
            # parse the NameList
            print(str(tmp))

        elif grm_name == 'Translation':
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

        elif grm_name == 'Publishers':
            tmp = result.find(PublisherList)
            # parse the PublisherList
            print(tmp)

        elif grm_name == 'Language':
            tmp = result.find(Word)
            # get the language
            print(tmp)

        elif grm_name == 'Other':
            tmp = result.find(Words)
            # parse the PublisherList
            print(tmp)

'''
