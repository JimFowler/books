#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Series/asslKluwer_table.py
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
  asslKluwer_table.py

   Table listing of the book series Astrophysics and Space Science
   Library published by Kluwer Academic 1965-1999 and by
   Springer after 2000.  This is information used
   with the book project "Some Important Books in Astronomy
   and Astrophysics in the 20th Century"

   This file creates the LaTeX longtable format
   asslKluwer_table.tex

   This information was gather from the back pages of
   volumes 280 and 338.
'''

from __future__ import print_function

import table as tb

tbl_comment = '''%%
%%
%% asslKluwer_table.tex
%%
%%   Table listing of the book series Astrophysics and Space Science
%%   Library published by Kluwer Academic 1965-1999 and by
%%   Springer after 2000.  This is information used
%%   with the book project "Some Important Books in Astronomy
%%   and Astrophysics in the 20th Century"
%%
'''

tbl_copyright = r'''%%   Copyright 2018 James R. Fowler
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

tbl_caption = r'\bf Kluwer \bt{Astrophysics and Space Science Library}'
tbl_format = r'[p]{l l l l}'
tbl_label = r'assl-kluwer:1'
tbl_heading = r'Vol & Title & Author/Editor(s) & Date'
continue_label = r'Continuation of \bt{Astrophysics and Space Science Library}'
tbl_footer = r''
continue_footer = r''

assl_book_list = [
    #( volnum, [title_list], 'copyright',
    # [authors/editors list],
    #'E|A', 'ISBN' )
    (216, ['Magnetohydrodynamics in',
           'Binary Stars'], '1997-08',
     ['C. G. Campbell'],
     'A', '0-7923-4606-8'),

    (217, ['Nonequilibrium Processes',
           'in the Planetary and Cometary',
           'Atmospheres'], '1997-09',
     ['Mikhail Ya. Marov', 'Valery I. Shematovich', 'Dmitry V. Bisikalo',
      'Jean-Claude Gérard'],
     'A', '0-7923-4686-6'),

    (218, ['Astronomical Time Series'], '1997-08',
     ['Dan Maoz', 'Amiel Sternberg', 'Elia M. Leibowitz'],
     'E', '0-7923-4706-4'),

    (219, ['The Interstellar Medium in Galaxies'], '1997-10',
     ['J. M. van der Hulst'],
     'E',  '0-7923-4676-9'),

    (220, ['The Three Galileos:',
           'The Man, The Spacecraft,',
           'The Telescope'], '1997-12',
     ['Cesare Barbiere', 'Jürgen H. Rahe', 'Torrence V. Johnson',
      'Anita M. Sohus'],
     'E', '0-7923-4861-3'),

    (221, [], None,
     [],
     None, None),

    (222, ['Remembering Edith Alice Müller'], '1998-02',
     ['Immo Appenzeller', 'Yves Chmielewski', 'Jean-Claude Pecker', 'Ramiro de la Reza',
      'Gustav Tammann', 'Patrick A. Wayman'],
     'E', '0-7923-4789-7'),

    (223, ['Visual Double Stars: Formation,',
           'Dynamics and Evolutionary Tracks'], '1997-11',
     ['J. A. Docobo', 'A. Elipe', 'H. McAlister'],
     'E', '0-7923-4793-5'),

    (224, ['Electronic Publishing for',
           'Physics and Astronomy'], '1997-09',
     ['André Heck'],
     'E', '0-7923-4820-6'),

    (225, ["SCORe'96: Solar Convection",
           'and Oscillations and Their',
           'Relationship'], '1998-01',
     ['F. P. Pijpers', 'Jøgen Christensen-Dalsgaard', 'C. S. Rosenthal'],
     'E', '0-7923-4852-4'),

    (226, ['Observational Cosmology with',
           'the New Radio Surveys'], '1998-02',
     ['M. N. Bremer', 'N. Jackson', 'I. Pérez-Fournon'],
     'E', '0-7923-4885-0'),

    (227, ['Solar System Ices'], '1998-01',
     ['B. Schmitt', 'C. de Bergh', 'M. Festou'],
     'E', '0-7923-4902-4'),

    (228, ['Optical Detectors for Astronomy'], '1998-04',
     ['James W. Beletic', 'Paola Amico'],
     'E', '0-7923-4925-3'),

    (229, ['Observational Plasma Astrophysics:',
           'Five Years of Yohkoh and Beyond'], '1998-03',
     ['Tetsuya Watanabe', 'Takeo Kosugi', 'Alphonse C. Sterling'],
     'E', '0-7923-4985-7'),

    (230, ['The Impact of Near Infrared',
           'Sky Surveys on Galactic and',
           'Extragalactic Astronomy'], '1998-06',
      ['N. Epchtein'],
     'E', '0-7923-5025-1'),

    (231, ['The Evolving Universe:',
           'Selected Topics on Large-Scale',
           'Structure and on the Properties',
           'of Galaxies'], '1998-07',
     ['Donald Hamilton'],
     'E', '0-7923-5074-X'),

    (232, ['The Brightest Binaries'], '1998-07',
     ['Dany Vanbeveren', 'W. van Rensbergen', 'C. W. H. de Loore'],
     'A', '0-7923-5155-X'),

    (233, ['B[e] Stars'], '1998-09',
     ['Anne Marie Hubert', 'Carlos Jaschek'],
     'E', '0-7923-5208-4'),

    (234, ['Observational Evindence for',
           'Black Holes in the Universe'], '1998-11',
     ['Sandip K. Chakrabarti'],
     'E', '0-7923-5298-X'),

    (235, ['Astrophysical Plasmas and Fluids'], '1999-01',
     ['Vinod Krishan'],
     'A', '0-7923-5312-9'),

    (236, ['Laboratory Astrophysics',
           'and Space Research'], '1998-12',
     ['P. Ehrenfreund', 'C. Krafft', 'H. Kochan', 'V. Pirronello'],
     'E', '0-7923-5338-2'),

    (237, ['Post-Hipparcos Cosmic Candles'], '1998-12',
     ['André Heck', 'Filippina Caputo'],
     'E', '0-7923-5348-X'),

    (238, ['Substorms-4'], '1999-03',
     ['S. Kokubun', 'Y. Kamide'],
     'E', '0-7923-5465-6'),

    (239, ['Motions in the Solar Atmosphere'], '1999-02',
     ['Arnold Hanslmeier', 'Mauro Meserotti'],
     'E', '0-7923-5507-5'),

    (240, ['Numerical Astrophysics'], '1999-03',
     ['Shoken M. Miyama', 'Kohji Tomisaka', 'Tomoyuki Hanawa'],
     'E', '0-7923-5566-0'),

    (241, ['Millimeter-Wave Astronomy:',
           'Molecular Chemistry',
           'and Physics in Space'], '1999-05',
     ['W. F. Wall', 'Alberto Carramiñana', 'Luis Carrasco', 'P. F. Goldsmith'],
     'E', '0-7923-5581-4'),

    (242, ['Cosmic Perspectives in Space Physics'], '2000-06',
     ['Sukumar Biswas'],
     'A', '0-7923-5813-9'),

    (243, ['Solar Polarization'], '1999-07',
     ['K. N. Nagendra', 'Jan Olof Stenflo'],
     'E', '0-7923-5814-7'),

    (244, ['The Universe:',
           'Visions and Perspectives'], '2000-08',
     ['Naresh Dadhich', 'Ajit Kembhavi'],
     'E', '0-7923-6210-1'),

    (245, ['Waves in Dusty Space Plasmas'], '2000-04',
     ['Frank Verheest'],
     'A', '0-7923-6232-2'),

    (246, ['The Legacy of J. C. Kapteyn:',
           'Studies on Kapteyn and the',
           'Development of Modern Astronomy'], '2000-08',
     ['Piet C. van der Kruit', 'Klaas van Berkel'],
     'E', '0-7923-6393-0'),

    (247, ['Large Scale Structure Formation'], '2000-08',
     ['Reza Mansouri', 'Robert Brandenberger'],
     'E', '0-7923-6411-2'),

    (248, [], None,
     [],
     None, None),

    (249, ['The Neutral Upper Atmosphere'], '2002',
     ['S. N. Gosh'],
     'A', '0-7923-6434-1'),

    (250, ['Information Handling in Astronomy'], '2000-10',
     ['André Heck'],
     'E', '0-7923-6494-5'),

    (251, ['Cosmic Plasma Physics'], '2000-09',
     ['Boris V. Somov'],
     'A', '0-7923-6512-7'),

    (252, ['Optical Detectors in Astronomy II:',
           'State-of-the-art at the Turn',
           'of the Millennium'], '2000-12',
     ['Paola Amico', 'James W. Beletic'],
     'E', '0-7923-6536-4'),

    (253, ['The Chemical Evolution of the Galaxy'], '2001-05',
     ['Francesca Matteucci'],
     'A', '0-7923-6552-6'),

    (254, ['Stellar Astrophysics'], '2000-11',
     ['K. S. Cheng', 'Hoi Fung Chau', 'Kwing Lam Chan', 'Kam Ching Leung'],
     'E', '0-7923-6659-X'),

    (255, ['The Evolution of the Milky Way:',
           'Stars versus Clusters'], '2001-01',
     ['Francesca Matteucci', 'Franco Giovannelli'],
     'E', '0-7923-6679-4'),

    (256, ['Organizations and Strategies',
           'in Astronomy'], '2000-11',
     ['André Heck'],
     'E', '0-7923-6671-9'),

    (257, ['Stellar Pulsation ---',
           'Nonlinear Studies'], '2001-03',
     ['Mine Takeuti', 'Dimitar D. Sasselov'],
     'E', '0-7923-6818-5'),

    (258, ['Electrohydrodynamics in Dusty',
           'and Dirty Plasmas:',
           'Gravito-Electrodynamics and EHD'], '2001-06',
     ['Hiroshi Kikuchi'],
     'A', '0-7923-6822-3'),

    (259, ['The Dynamic Sun'], '2001-05',
     ['Arnold Hanslmeier', 'Mauro Messerotti', 'Astrid Veronig'],
     'E', '0-7923-6915-7'),

    (260, ['Solar Cosmic Rays'], '2001-05',
     ['Leonty I. Miroshnichenko'],
     'A', '0-7923-6928-9'),

    (261, ['Collisional Process in the',
           'Solar System'], '2001-05',
     ['Mikhail Ya. Marov', 'Hans Rickman'],
     'E', '0-7923-6946-7'),

    (262, ['Whistler Phenomena',
           'Short Impulse Propogation'], '2001-06',
     ['Csaba Ferencz', 'Orsolya E. Ferencz', 'Dániel Hamar', 'János Lichtenberger'],
     'A', '0-7923-6995-5'),

    (263, [], None,
     [],
     None, None),

    (264, ['The Influence of Binaries',
           'on Stellar Population Studies'], '2001-07',
     ['Dany Vanbeveren'],
     'E', '0-7923-7104-6'),

    (265, ['Post-AGB Objects as a Phase',
           'of Stellar Evolution'], '2001-07',
     ['R. Szczerba', 'S. K. Góny'],
     'E', '0-7923-7145-3'),

    (266, ['Organizations and Stategies',
           'in Astronomy II'], '2001-10',
     ['André Heck'],
     'E', '0-7923-7172-0'),

    (267, ['The Nature of the Unidentified',
           'Galactic High-Energy',
           'Gamma-Ray Sources'], '2001-10',
     ['Alberto Carramiñana', 'Olag Reimer', 'David J. Thompson'],
     'E', '1-4020-0010-3'),

    (268, ['Multielement System Design in',
           'Astronomy and Radio Science'], '2001-11',
     ['Lazarus E. Kopilovich', 'Leonid G. Sodin'],
     'A', '1-4020-0069-3'),

    (269, ['Mechanics of Turbulence of',
           'Multicomponent Gases'], '2001-12',
     ['Mikhail Ya. Marov', 'Aleksander V. Kolesnichenko'],
     'A', '1-4020-0103-7'),

    (270, [], None,
     [],
     None, None),

    (271, ['Astronomy-inspired Atomic',
           'and Molecular Physics'], '2002-03',
     ['A. R. P. Rau'],
     'A', '1-4020-0467-2'),

    (272, ['Merging Processes in Galaxy Clusters'], '2002-05',
     ['L. Fretti', 'I. M. Gioia', 'G. Giovannini'],
     'E', '1-4020-0531-8'),

    (273, ['Lunar Gavimetry'], '2002-05',
     ['Rune Floberghagen'],
     'A', '1-4020-0544-X'),

    (274, ['New Quests in Stellar Astrophysics:',
           'The Link Between Stars',
           'and Cosmology'], '2002-06',
     ['Miguel Chávez', 'Alessandro Bressan',
      'Alberto Buzzoni', 'Divakara Mayya'],
     'E', '1-4020-0644-6'),

    (275, ['History of Oriental Astronomy'], '2002-12',
     ['S. M. Razaullah Ansari'],
     'E', '1-4020-0657-8'),

    (276, ['Modern Theoretical and',
           'Observational Cosmology'], '2002-09',
     ['Manolis Plionis', 'Spiros Cotsakis'],
     'E', '1-4020-0808-2'),

    (277, ['The Sun and Space Weather'], '2002-07',
     ['Arnold Hanslmeier'],
     'A', '1-4020-0684-5'),

    (278, ['Exploring the Secrets of the Aurora'], '2002-08',
     ['Syun-Ichi Akasofu'],
     'A', '1-4020-0685-3'),

    (279, ['Plasma Astrophysics,',
           '2nd edition'], '2002-07',
     ['Arnold O. Benz'],
     'A', '1-4020-0695-0'),

    (280, ['Organizations and Strategies',
           'in Astronomy III'], '2002-09',
     ['Andrë Heck'],
     'E', '1-4020-0812-0'),

    (281, ['The IGM/Galaxy Connection'], '2002-04',
     ['Jessica L. Rosenberg', 'Mary E. Putnam'],
     'E', '1-4020-1289-6'),

    (282, ['Radio Recombination Lines'], '2002-11',
     ['M. A. Gordon', 'R. L. Sorochenko'],
     'A', '1-4020-1016-8'),

    (283, ['Mass-Losing Pulsating Stars',
           'and Their Circumstellar Matter'], '2003-03',
     ['Y. Nakada', 'M. Honma', 'M. Seki'],
     'E', '1-4020-1162-8'),

    (284, ['Light Pollution: The Global View'], '2003-04',
     ['Hugo E. Schwartz'],
     'E', '1-4020-1174-1'),

    (285, ['Information Handling in Astronomy',
           '--- Historical Vistas'], '2003-03',
     ['Andrë Heck'],
     'E', '1-4020-1178-4'),

    (286, ['Searching the Heavens and the Earth:',
           'The Early History of',
           'Jesuit Observatories'], '2003-10',
     ['Augustín Udías'],
     'A', '1-4020-1189-X'),

    ('287/8/9', ['The Future of Small Telescopes',
                 'in the New Millennium'], '2003-07',
     ['Terry D. Oswalt'],
     'E', '1-4020-0951-8'),

    (290, ['Astronomy Communications'], '2003-07',
     ['André Heck', 'Claus Madsen'],
     'E', '1-4020-1345-0'),

    (291, ['Dynamical Systems and Cosmology'], '2003-11',
     ['Alan Coley'],
     'A', '1-4020-1403-1'),

    (292, ['Whatever Shines Should be Observed'], '2003-09',
     ['Susan M. P. McKenna-Lawlor'],
     'A', '1-4020-1424-4'),

    (293, ['Physics of the Solar System'], '2003-08',
     ['Bruno Bertotti', 'Paolo Farinella', 'David Vohrouhlický'],
     'A', '1-4020-1428-7'),

    (294, ['An Introduction to Plasma',
           'Astrophysics and',
           'Magnetohydrodynamics'], '2003-08',
     ['Marcel Goossens'],
     'A', '1-4020-1429-5'),
    
    (295, ['Itegrable Problems of Celestial',
           'Mechanics in Spaces of Constant',
           'Curvature'], '2003-10',
     ['T. G. Vozmischeva'],
     'A', '1-4020-1521-6'),

    (296, ['Organizations and Strategies',
           'in Astronomy, volume 4'], '2003-10',
     ['André Heck'],
     'E', '1-4020-1526-7'),

    (297, ['Radiation Hazard in Space'], '2003-09',
     ['Leonty I. Miroshnichenko'],
     'A', '1-4020-1538-0'),

    (298, ['Stellar Astrophysics --- A',
           'Tribute to Helmut A. Abt'], '2003-11',
     ['K. S. Cheng', 'Kam Ching Leung', 'T. P. Li'],
     'E', '1-4020-1683-2'),

    (299, ['Open Issues in Local',
           'Star Formation'], '2003-12',
     ['Jacques Lépine', 'Jane Gregorio-Hetem'],
     'E', '1-4020-1755-3'),

    (300, ['Scientific Detectors',
           'for Astronomy'], '2004-02',
     ['Paola Amica', 'James W. Beletic', 'Jenna E. Beletic'],
     'E', '1-4020-1788-X'),

    (301, ['Multiwavelength Cosmology'], '2004-03',
     ['Manolis Plionis'],
     'E', '1-4020-1971-8'),

    (302, ['Stellar Collapse'], '2004-04',
     ['Chris L. Fryer'],
     'E', '1-4020-1992-0'),

    (303, ["Cosmic rays in the Earth's",
           "Atmosphere and Underground"], '2004-08',
     ['L. I. Dorman'],
     'A', '1-4020-2071-6'),

    (304, ['Cosmic Gamma-ray Sources'], '2004-09',
     ['K. S. Cheng', 'G. E. Romero'],
     'E', '1-4020-2255-7'),

    (305, ['Astrobiology: Future Perspectives'], '2004-07',
     ['P. Ehrenfreund', 'W. M. Irvine', 'T. Owen', 'L. Becker',
      'J. Blank', 'J. R. Brucato', 'L. Colangeli', 'S. Derenne',
      'A. Dutrey', 'D. Despois', 'A. Lazcano', 'F. Robert'],
     'E', '1-40202304-9'),
    
    (306, ['Polytropes --- Applications in',
           'Astrophysics and Related Fields'], '2004-09',
     ['G. P. Horedt'],
     'A', '1-4020-2350-2'),

    (307, ['Polarization in Spectral Lines'], '2004-08',
     ["E. Landi Degl'Innocenti", 'M. Landolfi'],
     'A', '1-4020-2414-2'),

    (308, ['Supermasive Black Holes',
           'in the Distant Universe'], '2004-08',
     ['A. J. Barger'],
     'E', '1-4020-2470-3'),

    (309, ['Soft X-ray Emission from Cluster',
           'of Galaxies and Related Phenomena'], '2004-09',
     ['R. Lieu', 'J. Mittaz'],
     'E', '1-4020-2563-7'),

    (310, ['Organizations and Strategies',
           'in Astronomy 5'], '2004-09',
     ['A. Heck'],
     'E', '1-4020-2570-X'),

    (311, ['The New ROSETTA Targets',
           '--- Observations, Simulations',
           'and Instrument Performance'], '2004-09',
     ['L. Colangeli', 'E. Mazzotta Epifani', 'P. Palumbo'],
     'E', '1-4020-2572-6'),

    (312, ['High-Velocity Clouds'], '2004-09',
     ['H. van Woerden', 'U. Schwarz', 'B. Wakker'],
     'E', '1-4020-2813-X'),

    (313, ['Adventures in Order and Chaos'], '2005-01',
     ['G. Contopoulos'],
     'A', '1-4020-3039-8'),

    (314, ['Solar and Space Weather',
           'Radiophysics --- Current',
           'Status and Future Developments'], '2004-08',
     ['D. E. Gary', 'C. U. Keller'],
     'E', '1-4020-2813-X'),

    (315, ['How does the Galaxy Work',
           '--- A Galactic Tertulia with',
           'Don Cox and Ron Reynolds'], '2004-09',
     ['E. J. Alfaro', 'E. Pérez', 'J. Franco'],
     'E', '1-4020-2619-6'),

    (316, ['Civic Astronomy ---',
           "Albany's Dudley Observatory",
           "1852--2002"], '2004-10',
     ['G. Wise'],
     'A', '1-4020-2677-3'),

    (317, ['The Sun and the Heliosphere',
           'as an Integrated System'], '2004-11',
     ['G. Poletto', 'S. T. Suess'],
     'E', '1-4020-2830-X'),

    (318, ['Transfer of Polarized light',
           'in Planetary Atmospheres'], '2004-11',
     ['J. W. Hovenier', 'J. W. Domke', 'C. van der Mee'],
     'A', '1-4020-2855-5'),

    (319, ['Penetrating Bars through',
           'Masks of Cosmic Dust'], '2004-12',
     ['D. L. Block', 'I.Puerari', 'K. C. Freeman', 'R. Groess', 'E. K. Block'],
     'E', '1-4020-2861-X'),

    (320, ['Solar Magnetic Phenomena'], '2004-12',
     ['A. Hanslmeier', 'A. Veronig', 'M. Messerotti'],
     'E', '1-4020-2961-6'),

    (321, ['Nonequilibrium Phenomena',
           'in Plasmas'], '2004-12',
     ['A. S. Shrama', 'P. K. Kaw'],
     'E', '1-4020-3108-4'),
    
    (322, ['Light Pollution Handbook'], '2004-11',
     ['K. Narisada', 'D. Schreuder'],
     'A', '1-4020-2665-X'),

    (323, ['Recollections of Tucson Operations'], '2004-11',
     ['M. A. Gordon'],
     'A', '1-4020-3235-8'),

    (324, ['Cores to Clusters ---',
           'Star Formation with',
           'next Generation Telescopes'], '2005-10',
     ['M. S. Nanda Kumar', 'M. Tafalla', 'P. Caselli'],
     'E', '0-387-26322-5'),

    (325, ['Kristian Birkeland ---',
           'The First Space Scientist'], '2005-04',
    ['A. Egeland', 'W. J. Burke'],
    'A', '1-4020-3293-5'),

    (326, [], None,
     [],
     None, None),

    (327, ['The Initial Mass Function',
           '50 Years Later'], '2005-06',
     ['E, Corbelli', 'F. Palla', 'H. Zinnecker'],
     'E', '1-4020-3406-7'),

    (328, ['Comets'], '2005-07',
     ['J. A. Fernández'],
     'A', '1-4020-3490-3'),

    (329, ['Starbursts ---',
           'From 30 Doradus',
           'to Lyman Break Galaxies'], '2005-05',
     ['R. de Grijs', 'R. M. González Delgado'],
     'E', '1-4020-3538-1'),

    (330, ['The Multinational History',
           'of Stasborg Astronomical',
           'Observatory'], '2005-06',
     ['A. Heck'],
     'A', '1-4020-3643-4'),

    (331, ['Ultraviolet Radiation in',
           'the Solar System'], '2005-11',
     ['M. Vázquez', 'A. Hanslmeier'],
     'A', '1-4020-3726-0'),

    (332, ['White Dwarfs: Cosmological',
           'and Galactic Probes'], '2005-09',
     ['E. M. Sion', 'S. Vennes', 'H. L. Shipman'],
     'E', '1-4020-3693-0'),

    (333, ['Planet Mercury'], '2005-11',
     ['P. Clark', 'S. McKenna-Lawlor'],
     'A', '1-387-26358-6'),

    (334, ['The New Astronomy:',
           'Opening the Electromagnetic',
           'Window and Expanding Our',
           'View of Planet Earth'], '2005-10',
     ['W. Orchiston'],
     'E', '1-4020-3723-6'),

    (335, ['Organization and Strategies',
           'in Astronomy 6'], '2005-11',
     ['A. Heck'],
     'E', '1-4020-4055-5'),

    (336, ['Scientific Detectors',
           'for Astronomy 2005'], '2005-12',
     ['J. E. Beletic', 'J. W. Beletic', 'P. Amico'],
     'E', '1-4020-4329-5'),

    (337, ['Progress in the Study',
           'of Astrophysical Disks'], '2006-03',
     ['A. M. Fridman', 'M. Y. Marov', 'I. G. Kovalenko'],
     'E', '1-4020-4347-3'),

    (338, ['Solar Journey:',
           'The Significance of our',
           'Galactic Environment for',
           'the Heliosphere and Earth'], '2006-05',
     ['P. C. Frisch'],
     'E', '1-4020-4397-X'),

]


def assl_print_books(book_list):
    for volnum, title_list, year, author_list, ae_flag, isbn in book_list:
        len_title = len(title_list)
        len_author = len(author_list)
        max_loops = max(len_title, len_author, 1)

        raw_str = r''
        
        # Do first line
        for index in range(1, max_loops+1):
            if volnum is not None:
                raw_str += r'''  {0} & '''.format(volnum)
                volnum = None
            else:
                raw_str += r'''  & '''

            if len_title >= index:
                raw_str += r'''\bt{}{}{} & '''.format('{', title_list[index-1], '}')
            else:
                raw_str += r''' & '''

            if len_author >= index:
                raw_str += r'''{} & '''.format(author_list[index-1])
            else:
                raw_str += r''' & '''

            if year is not None:
                raw_str += r'''{}'''.format(year)
                year = None

            if index == max_loops:
                # at the end of a book allow a break and add spacing
                raw_str += r''' \\[5pt]'''
            else:
                raw_str += r''' \\*'''
                
            raw_str += '''
'''
        # Clean up for TeX and print() statement
        raw_str2 = raw_str.replace( r'. ', r'.\ ')
        safe_str = tb.protect_str(raw_str2)
        # if more title and/or more authors
        print(safe_str)
    return

if __name__ == '__main__':

    tb.print_table_comment(tbl_comment)
    tb.print_table_copyright(tbl_copyright)
    tb.print_table_preamble('')
    tb.print_table_start(tbl_format)

    tb.print_table_caption(tbl_caption)
    tb.print_table_label(tbl_label)
    tb.print_table_heading(4, tbl_heading, continue_label)
    tb.print_table_footer(tbl_footer, continue_footer)

    assl_print_books(assl_book_list)
    tb.print_table_end()

