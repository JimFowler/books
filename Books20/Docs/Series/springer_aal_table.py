#! /usr/bin/env python3
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Series/Springer/aal_table.py
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
'''
  aal_table.py

  Table listing of the book series Astronomy and Astrophysics Library
  published by Springer-Verlag from 1978 to the present.

  This file created the LaTeX longtable format
  springer_aal_table.tex.
'''
import table as tb
from pprint import pprint

TBL_COMMENT = '''%%
%%
%% asslKluwerTable.tex
%%
%%   Table listing of the book series Astronomy and Astrophysics
%%   Library published Springer-Verlag. This is information used
%%   with the book project "Some Important Books in Astronomy
%%   and Astrophysics in the 20th Century"
%%
'''

TBL_COPYRIGHT = r'''%%   Copyright 2018 James R. Fowler
%%
%%   All rights reserved. No part of this publication may be
%%   reproduced, stored in a retrival system, or transmitted
%%   in any form or by any means, electronic, mechanical,
%%   photocopying, recording, or otherwise, without prior written
%%   permission of the author.
%%
%%
%%
'''

TBL_CAPTION = r'\bfseries Springer \bt{Astronomy and Astrophysics Library}'
TBL_FORMAT = r'[p]{l l l}'
TBL_LABEL = r'aal-springer:1'
TBL_HEADING = r'Title & Author/Editor(s) & Date'
CONTINUE_LABEL = r'Continuation of \bt{Astronomy and Astrophysics Library}'
TBL_PREAMBLE = r'''\setlength\LTleft{0pt}'''
TBL_FOOTER = r''
CONTINUE_FOOTER = r''

AAL_BOOK_LIST = [
    #(volnum, [title_list], 'copyright',
    # [authors/editors list],
    #'E|A', 'ISBN'),
    (1, ['Astrophysical Formulae:', 'Space, Time, Matter and Cosmology, \Ord{2}{nd} ed.',], '1978', 
     ['Kenneth R. Lang'],
     'A', None),

    (2, ['Galactic and Extragalactic Radio', 'Astronomy, \Ord{2}{nd} ed.'], '1988', 
     ['Gerrit L. Verschuur', 'Kenneth I. Kellermann'],
     'E', None),

    (3, ['Physics of the Galaxy and', 'Interstellar Matter'], '1988', 
     ['Helmut Scheffler', 'Hans Elsässer'],
     'A', None),

    (4, ['Astrophysical Concepts, \Ord{2}{nd} ed.'], '1988', 
     ['Martin Harwit'],
     'A', None),

    (5, ['Observational Astrophysics'], '1988', 
     ['Pierre Léna'],
     'A', None),

    (6, ['The Sun:', 'An Introduction'], '1989', 
     ['Michael'],
     'E', None),

    (7, ['Relativity in Astrometry,', 'Celestial Mechanics and Geodesy'], '1989', 
     ['Michael H. Soffel'],
     'A', None),

    (8, ['Supernovae'], '1990', 
     ['Albert G. Petschek'],
     'E', None),

    (9, ['Stellar Structure and Evolution'], '1990', 
     ['Rudolf Kippenhahn', 'Alfred Weigert'],
     'A', None),

    (10, ['Physics and Chemistry of Comets'], '1990', 
     ['Walter F. Huebner'],
     'E', None),

    (11, ['Gravitational Lenses'], '1992', 
     ['Peter Schneider', 'Jürgen Ehlers', 'Emilio E. Falco'],
     'A', None),

    (12, ['General Relativity, Astrophyiscs,', 'and Cosmology'], '1992',
     ['A.~K. Raychaudhuri','S. Banerji', 'A. Banerjee'],
     'A', None),
    
    (13, ['Astrophysics of Neutron Stars', '(translated from the Russian)'], '1992',
     ['Valdimir M. Lipunov'],
     'A', None ),

    (14, ['The Stars'], '1993',
     ['Evry L. Schatzman', 'Francoise Praderie'],
     'A', None),
    
    (15, ['Stellar Interiors:', 'Physical Principles, Structure,',
          'and Evolution'], '1994', 
     ['Carl J. Hansen', 'Steven D. Kawaler'],
     'A', None),

    (16, ['Atoms in Strong Magnetic Fields:', 'Quantum Mechanical Treatments',
          'and Applications in Astrophyics', 'and Quantum Chaos'], '1994', 
     ['Hanns Ruder', 'Günter Wunner', 'Heinz Herold', 'Florian Geyer'],
     'A', None),

    (17, ['Modern Astrometry'], '1995', 
     ['Jean Kovalevsky'],
     'A', None),

    (18, ['The Solar System, \Ord{2}{nd} ed.'], '1995', 
     ['Thérèse Encrenaz', 'Jean-Pierre Bibring'],
     'A', None),

    (19, ['Galaxies and Cosmology'], '1995',
    ['F. Combes', 'P. Boissé', 'A. Mazure', 'A. Blanchard'],
     'A', None),

    (20, ['Reflecting Telescope Optics:', 'Part I, Basic Design Theory and its',
          'Historical Development'], '1996', 
     ['Raymond N. Wilson'],
     'A', None),

    (21, ['Theory of Orbits:', 'Vol. 1, Integrable Systems and',
          'Non-perturbative Methods'], '1996', 
     ['Dino Boccaletti', 'Giuseppe Pucacco'],
     'A', None),

    (22, ['Compact Stars:', 'Nuclear Physics, Particle Physics',
          'and General Relativity'], '1997', 
     ['Norman K. Glendenning'],
     'E', None),

    (23, ['The Physics and Dynamics of', 'Planetary Nebulae'], '1997', 
     ['Grigor A. Gurzadyan'],
     'A', None),

    (24, ['Astrophysical Concepts, \Ord{3}{rd} ed.'], '1998', 
     ['Martin Harwit'],
     'A', None),

    (25, ['Galaxy Formation'], '1998', 
     ['Malcolm S. Longair'],
     'A', None),

    (26, ['Observational Astrophysics, \Ord{2}{nd} ed.'], '1998', 
     ['Pierre Léna', 'François Lebrun', 'François Mignard'],
     'A', None),

    (27, ['Theory of Orbits:', 'Vol. 2, Perturbative and Geometrical', 'Methods'], '1999', 
     ['Dino Boccaletti', 'Giuseppe Pucacco'],
     'A', None),

    (28, ['Physics of Planetary Rings:', 'Celestial Mechanics of Continuous',
          'Media'], '1999', 
     ['Alexei M. Fridman', 'Nikolai N. Gorkavyi'],
     'A', None),

    (29, ['Reflecting Telescope Optics:', 'Part 2, Manufacturing, Testing,',
          'Alignment, Modern Techniques'], '1999', 
     ['Raymond N. Wilson'],
     'A', None),

    (30, ['Compact Stars, \Ord{2}{nd}:', 'Nuclear Physics, Particle Physics',
          'and General Relativity'], '2000', 
     ['Norman K. Glendenning'],
     'E', None),

    (31, ['Astrometry of Fundamental Catalogues:', 'The Evolution from Optical to Radio',
          'Reference Frames'], '2000', 
     ['Hans G. Walter', 'Ojars J. Sovers'],
     'A', None),

    (32, ['Tools of Radio Astronomy:', 'Problems and Solutions'], '2000', 
     ['Thomas L. Wilson', 'Susanne Hüttemeister'],
     'A', None),

    (33, ['The Sun from Space'], '2000', 
     ['Kenneth R. Lang'],
     'A', None),

    (34, ['Black Hole Gravitohydromagnetics'], '2001', 
     ['Brian Punsly'],
     'A', None),

    (35, ['The Universe in Gamma Rays'], '2001', 
     ['Volker Schönfelder'],
     'E', None),

    (36, ['Astrophysics:', 'A Primer'], '2001', 
     ['Wolfgang Kundt'],
     'A', None),

    (37, ['Interplanetary Dust:', 'Volume 1'], '2001', 
     ['Eberhard Grün', 'Bo Å. S. Gustafson', 'Stan Dermott', 'Hugo Fechtig'],
     'E', None),

    (38, ['Stellar Physics:',
          'Volume 1, Fundamental Concepts and Stellar Evolution'], '2001', 
     ['G. S. Bisnovatyi-Kogan'],
     'A', '978-3-540-63262-7'),

    (39, ['The Sun: An Introduction, \Ord{2}{nd} ed.'], '2002', 
     ['Michael Stix'],
     'A', None),

    (40, ['Modern Astrometry, \Ord{2}{nd} ed.'], '2002', 
     ['Jean Kovalevsky'],
     'A', None),

    (41, ['Astronomical Image and Data Analysis'], '2002', 
     ['Jean-Luc Starck', 'Fionn Murtagh'],
     'A', None),

    (42, ['Order and Chaos in Dynamical', 'Astronomy'], '2002', 
     ['George Contopoulos'],
     'A', None),

    (43, ['Stellar Physics:', 'Volume 2, Stellar Evolution and', 'Stability'], '2002', 
     ['G. S. Bisnovatyi-Kogan'],
     'A', None),

    (44, ['Cosmic Ray Astrophysics'], '2002', 
     ['Reinhard Schlickeiser'],
     'A', None),

    (45, ['Galaxies and Cosmology, \Ord{2}{nd} ed.'], '2002',
    ['F. Combes', 'P. Boissé', 'A. Mazure', 'A. Blanchard'],
     'A', '978-3-540-41927-3'),

    (46, ['Astrophysics of the Diffuse Universe'], '2003', 
     ['Michael A. Dopita', 'Ralph S. Sutherland'],
     'A', None),

    (47, ['The Early Universe:', 'Facts and Fiction, \Ord{4}{th} ed.'], '2003', 
     ['Gerhard Börner'],
     'A', None),

    (48, ['The Design and Construction of', 'Large Optical Telescopes'], '2003', 
     ['Pierre Y. Bely'],
     'A', None),

    (49, ['Tools of Radio Astronomy, \Ord{4}{th} ed.'], '2004', 
     ['K. Rohlfs', 'T. L. Wilson'],
     'A', None),

    (50, ['Asymptotic Giant Branch Stars'], '2004', 
     ['Harm J. Habing', 'Hans Olofsson'],
     'E', None),

    (51, ['Stellar Interiors:', 'Physical Principles, Structure,',
          'and Evolution, \Ord{2}{nd} ed.'], '2004', 
     ['Carl J. Hansen', 'Steven D. Kawaler', 'Virginia Trimble'],
     'A', None),

    (52, ['The Solar System, \Ord{3}{rd} ed.'], '2004', 
     ['Thérèse Encrenaz', 'Jean-Pierre Bibring', 'Michel Blanc', 'Maria-Antonietta Barucci',
      'Francoise Roques', 'Philippe Zarka'],
     'A', None),

    (53, ['Reflecting Telescope Optics:', 'Part 1, Basic Design Theory and its',
          'Historical Development, \Ord{2}{nd} ed.'], '2004', 
     ['Raymond N. Wilson'],
     'A', None),

    (54, ['Solar-Type Activity in Main-Sequence', 'Stars'], '2005', 
     ['Roald E. Gershberg'],
     'A', None),

    (55, ['The Interstellar Medium'], '2005', 
     ['James Lequeux'],
     'A', None),

    (56, ['Methods of Celestial Mechanics:', 'Vol. 1, Physical, Mathematical, and',
          'Numerical Principles'], '2005', 
     ['Gerhard Beutler'],
     'A', None),

    (57, ['Methods of Celestial Mechanics:', 'Vol. 2, Application to Planetary',
          'Systems, Geodynamics and Satellite', 'Geodesy'], '2005', 
     ['Gerhard Beutler'],
     'A', None),

    (58, ['Astrophysics:', 'A New Approach, \Ord{2}{nd} ed.'], '2005', 
     ['Wolfgang Kundt'],
     'A', None),

    (59, ['Astrophysical Concepts, \Ord{4}{th} ed.'], '2006', 
     ['Martin Harwit'],
     'A', None),

    (60, ['Astronomical Image and Data Analysis,', '\Ord{2}{nd} ed.'], '2006', 
     ['J.-L. Starck', 'F. Murtagh'],
     'A', None),

    (61, ['Relativistic Astrophysics and', 'Cosmology:', 'A Primer'], '2006', 
     ['Peter Hoyng'],
     'A', None),

    (62, ['Magneto-Fluid Dynamics:', 'Fundamental and Case-Studies of',
          'Natural Phenomena'], '2006', 
     ['Paul Lorrain', 'François Lorrain', 'Stéphane Houle'],
     'A', None),

    (63, ['Special and General Relativity:', 'With Applications to White Dwarfs,',
          'Neutron Stars and Black Holes'], '2007', 
     ['Norman K. Glendenning'],
     'A', None),

    (64, ['Compact Objects in Astrophysics:', 'White Dwarfs, Neutron Stars and',
          'Black Holes'], '2007', 
     ['Max Camenzind'],
     'A', None),

    (65, ['Solar System Astrophysics:', 'Plantary Atmospheres and',
          'the Outer Solar System'], '2008', 
     ['Eugene F. Milone', 'Willam J. F. Wilson'],
     'A', None),

    (66, ['Solar System Astrophysics:', 'Background Science and',
          'the Inner Solar System'], '2008', 
     ['Eugene F. Milone', 'Willam J. F. Wilson'],
     'A', None),

    (67, ['Galaxy Formation, \Ord{2}{nd} ed.'], '2008', 
     ['Malcolm S. Longair'],
     'A', None),

    (68, ['The Universe in X-Rays'], '2008', 
     ['Joachim E. Trümper', 'Günther Hasinger'],
     'E', None),

    (69, ['High-Redshift Galaxies:', 'Light from the Early Universe'], '2009', 
     ['Immo Appenzeller'],
     'A', None),

    (70, ['Eclipsing Binary Stars:', 'Modeling and Analysis, \Ord{2}{nd} ed.'], '2009', 
     ['Josef Kallrath', 'Eugene F. Milone'],
     'A', None),

    (71, ['The Sun from Space, \Ord{2}{nd} ed.'], '2009', 
     ['Kenneth R. Lang'],
     'A', None),

    (72, ['Physics, Formation and Evolution of', 'Rotating Stars'], '2009', 
     ['André Maeder'],
     'A', None),

    (73, ['Tools of Radio Astronomy, \Ord{5}{th} ed.'], '2009', 
     ['Thomas L. Wilson', 'Kristen Rohlfs', 'Susanne Hüttemeister'],
     'A', None),

    (74, ['Planetary Systems:', 'Detection, Formation and',
          'Habitability of Extrasolar Planets'], '2009', 
     ['Marc Ollivier', 'Francoise Roques', 'Fabienne Casoli',
      'Thérèse Encrenaz', 'Franck Selsis'],
     'A', None),

    (75, ['Astronomical Optics and', 'Elasticity Theory:',
          'Active Optics Methods'], '2009', 
     ['Gérard René Lemaitre'],
     'A', None),

    (76, ['MHD Flows in Compact Astrophysical', 'Objects:',
          'Accretion, Winds and Jets'], '2010', 
     ['Vasily S. Beskin'],
     'A', None),

    (77, ['The Earth as a Distant Planet:', 'A Rosetta Stone for the Search of',
          'Earth-Like Worlds'], '2010', 
     ['M. VázquezE. Pallé', 'P. Montañés Rodríguez'],
     'A', None),

    (78, ['Asteroseismology'], '2010', 
     ['C. Aerts', 'J. Christensen-Dalsgaard', 'D. W. Kurtz'],
     'A', None),

    (79, ['Principles of Star Formation'], '2011', 
     ['Peter H. Bodenheimer'],
     'A', None),

    (80, ['Principles of Stellar Interferometry'], '2011', 
     ['Andreas Glindemann'],
     'A', None),

    (81, ['Stellar Physics:', 'Part 2, Stellar Evolution and',
          'Stability, \Ord{2}{nd} ed.'], '2011', 
     ['Gennady S. Bisnovatyi-Kogan'],
     'A', None),

    (82, ['Aperture Synthesis:', 'Methods and Applications to', 'Optical Astronomy'], '2011', 
     ['Swapan Kumar Saha'],
     'A', None),

    (83, ['The Formation and Early Evolution', 'of Stars:',
          'From Dust to Stars and Planets, \Ord{2}{nd} ed.'], '2012', 
     ['Norbert S. Schulz'],
     'A', None),

    (84, ['Chemical Evolution of Galaxies'], '2012', 
     ['Francesca Matteucci'],
     'A', None),

    (85, ['Observational Astrophysics, \Ord{3}{rd} ed.'], '2012', 
     ['Pierre Léna', 'Daniel Rouan', 'François Lebrun', 'François Mignard', 'Didier Pelat'],
     'A', None),

    (86, ['Stellar Structure and Evolution, \Ord{2}{nd} ed.'], '2012', 
     ['Rudolf Kippenhahn', 'Alfred Weigert', 'Achim Weiss'],
     'A', None),

    (87, ['High Energy Astrophysics:', 'An Introduction'], '2013', 
     ['Thierry J.-L. Courvoisier'],
     'A', None),

    (88, ['Space-Time Reference Systems'], '2013', 
     ['Michael Soffel', 'Ralf Langhans'],
     'A', None),

    (89, ['Tools of Radio Astronomy, \Ord{6}{th} ed.'], '2013', 
     ['Thomas L. Wilson', 'Kristen Rohlfs', 'Susanne Hüttemeister'],
     'A', '978-3-642-39949-7'),

    (90, ['An Introduction to Waves and', 'Oscillations in the Sun'], '2013', 
     ['A. Satya Narayanan'],
     'A', None),

    (91, ['Solar System Astrophysics:', 'Plantary Atmospheres and',
          'the Outer Solar System, \Ord{2}{nd} ed.'], '2014', 
     ['Eugene F. Milone', 'William J.F. Wilson'],
     'A', None),

    (92, ['Solar System Astrophysics:', 'Background Science and',
          'the Inner Solar System, \Ord{2}{nd} ed.'], '2014', 
     ['Eugene F. Milone', 'William J.F. Wilson'],
     'A', None),

    (93, ['Particles and Astrophysics:', 'A Multi-Messenger Approach'], '2015', 
     ['Maurizio Spurio'],
     'A', None),

    (94, ['Atomic Diffusion in Stars'], '2015', 
     ['Georges Michaud', 'Georges Alecian', 'Jacques Richer'],
     'A', None),

    (95, ['Introduction to Astrochemistry:', 'Chemical Evolution from Interstellar',
          'Clouds to Star and Planet Formation'], '2017', 
     ['Satoshi Yamamoto'],
     'A', None),

    (96, ['Interferometry and Synthesis in', 'Radio Astronomy, \Ord{3}{rd} ed.'], '2017', 
     ['A. Richard Thompson', 'James M. Moran', 'George W. Swenson Jr.'],
     'A', None),

    (97, ['Supernova Explosions'], '2017', 
     ['David Branch', 'J. Craig Wheeler'],
     'A', None),

    (98, ['Characterizing Space Plasmas:', 'A Data Driven Approach'], '2018', 
     ['George K. Parks'],
     'A', None),

    (99, ['Tools of Radio Astronomy -',
          'Problems and Solutions, \Ord{2}{nd} ed.'], '2018', 
     ['T.L. Wilson', 'Susanne Hüttemeister'],
     'A', None),

    (100, ['Probes of Multimessenger Astrophysics, \Ord{2}{nd} ed.:',
          'Changed cosmic rays, neutrinoes, $\gamma$-rays',
          'and gravitational waves'], '2018',
     ['Maurizio Spurio'],
     'A', '978-3-319-96853-7'),

    (101, ['Applied General Relativity:', 'Theory and Applications in Astronomy,',
          'Celestial Mechanics and Metrology'], '2019',
     ['Michael Soffel', 'Wen-Biao Han'],
     'A', '978-3-030-19672-1'),

    (102, ['The First Stars'], '2020',
     ['Volker Bromm'],
     'A', '978-3-642-11964-4'),
    ]

def aal_print_books(book_list):
    '''Print the book list in aal_table in long table format.'''
    for volnum, title_list, year, author_list, ae_flag, isbn in book_list:
        len_title = len(title_list)
        len_author = len(author_list)
        max_loops = max(len_title, len_author, 1)

        raw_str = r''
        # Do first line
        for index in range(1, max_loops+1):
            #if volnum is not None:
            #    raw_str += r'''  {0} & '''.format(volnum)
            #    volnum = None
            #else:
            #    raw_str += r'''  & '''

            if len_title >= index:
                raw_str += r'''\bt{}{}{} & '''.format('{', title_list[index-1], '}')
            else:
                raw_str += r''' & '''

            if len_author >= index:
                raw_str += r'''{} '''.format(author_list[index-1])
                if ae_flag == 'E' and index == 1:
                    raw_str += r'''eds. & '''
                else:
                    raw_str += r'''& '''
            else:
                raw_str += r''' & '''

            if year is not None:
                raw_str += r'''{}'''.format(year)
                year = None

            if isbn is not None:
                isbn = None


            if index == max_loops:
                # at the end of a book allow a break and add spacing
                raw_str += r''' \\[5pt]'''
            else:
                raw_str += r''' \\*'''

            raw_str += '''
'''
        # Clean up for TeX and print(), statement
        raw_str = raw_str.replace(r'. ', r'.\ ')
        safe_str = tb.protect_str(raw_str)
        # if more title and/or more authors
        print(safe_str)

if __name__ == '__main__':

    tb.print_table_comment(TBL_COMMENT)
    tb.print_table_copyright(TBL_COPYRIGHT)
    tb.print_table_preamble(TBL_PREAMBLE)
    tb.print_table_start(TBL_FORMAT)

    tb.print_table_caption(TBL_CAPTION)
    tb.print_table_label(TBL_LABEL)
    tb.print_table_heading(3, TBL_HEADING, CONTINUE_LABEL)
    tb.print_table_footer(TBL_FOOTER, CONTINUE_FOOTER)

    aal_print_books(AAL_BOOK_LIST)
    tb.print_table_end()

