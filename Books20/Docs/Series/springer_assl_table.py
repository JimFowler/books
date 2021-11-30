#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
## Begin copyright
##
##  /home/jrf/Documents/books/Books20/Docs/Series/assl_table.py
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
  assl_table.py

   Table listing of the book series Astrophysics and Space Science
   Library published by Kluwer Academic 1965-1999 and by
   Springer after 2000.  This is information used
   with the book project "Some Important Books in Astronomy
   and Astrophysics in the 20th Century"

   This file creates the LaTeX longtable format
   springerASSLtable.tex

   This information was gather from the back pages of
   volumes 280 and 338. The remaining data were collected
   from the Springer-Nature web site.

   Note that some of the works were published as multi-volume
   publications.
'''

import sys
import table as tb
from pprint import pprint

TBL_COMMENT = '''%%
%%
%% springerASSLtable.tex
%%
%%   Table listing of the book series Astrophysics and Space Science
%%   Library published by Kluwer Academic 1965-1999 and by
%%   Springer after 2000.  This is information used
%%   with the book project "Some Important Books in Astronomy
%%   and Astrophysics in the 20th Century"
%%
%%   Note that some of the works were published as multi-volume
%%   publications.
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

TBL_CAPTION = r'\bfseries Springer \bt{Astrophysics and Space Science Library}'
TBL_FORMAT = r'[p]{l l l l}'
TBL_LABEL = r'assl-springer:1'
TBL_HEADING = r'Vol & Title & Author/Editor(s) & Date'
CONTINUE_LABEL = r'Continuation of \bt{Astrophysics and Space Science Library}'
TBL_PREAMBLE = ''
TBL_FOOTER = r''
CONTINUE_FOOTER = r''

ASSL_BOOK_LIST = [
    #(volnum, [title_list], 'copyright',
    # [authors/editors list],
    #'E|A', 'ISBN', 'AJB/AAA num'),
    (1, ['The Solar Spectrum:', 'Proceedings of the Symposium held at',
         'the University of Utrecht 26–31', 'August 1963'], '1965', 
     ['C. De Jager'],
     'E', None, 'AJB 65.13.05'),

    (2, ['Introduction to Solar Terrestrial', 'Relations:',
         'Proceedings of Summer School in', 'Space Physics Held in Alpbach,',
         'Austria, July 15 – August 10, 1963', 'and Organized by the European',
         'Preparatory Commission for Space', 'Research (COPERS),'], '1965',
     ['J. Ortner', 'H. Maseland'],
     'E', None, 'AJB 65.13.04'),

    (3, ['Proceedings of the Plasma Space', 'Science Symposium:',
         'Held at the Catholic University of',
         'America Washington, D.C., June', '11–14, 1963'], '1965', 
     ['C. C. Chang', 'S. S. Huang'],
     'E', None, 'AJB 65.13.02'),

    (4, ['An Introduction to the Study of the', 'Moon'], '1966', 
     ['Zdeněk Kopal'],
     'A', None, 'AJB 66.83.125'),

    (5, ['Radiation Trapped in the Earth’s', 'Magnetic Field:',
         'Proceedings of the Advanced Study',
         'Institute Held at the Chr. Michelson',
         'Institute, Bergen, Norway August 16', '– September 3, 1065'], '1966', 
     ['Billy M. McCormac'],
     'E', None, 'AJB 66.13.33'),

    (6, ['The Early Type Stars'], '1966', 
     ['Anne B. Underhill'],
     'A', None, 'AJB 66.104.146'),

    (7, ['Introduction to Celestial Mechanics'], '1967', 
     ['Jean Kovalesky'],
     'A', '90-277-0398-1', 'AJB 67.41.52'),

    (8, ['Measure of the Moon:', 'Proceedings of the Second',
         'International Conference on',
         'Selenodesy and Lunar Topography held',
         'in the University of Manchester,',
         'England May 30 – June 4, 1966'], '1967', 
     ['Zdeněk Kopal', 'Constantine L. Goudas'],
     'E', None, 'AJB 67.13.25'),

    (9, ['Electromagnetic Radiation in Space:',
         'Proceedings of the Third ESRO Summer',
         'School in Space Physics, Held in',
         'Alpbach, Austria, from 19 July to 13', 'August, 1965'], '1967', 
     ['J. G. Emming'],
     'E', None, 'AJB 67.13.09'),

    (10, ['Physics of the Magnetosphere:', 'Based upon the Proceedings of the',
          'Conference Held at Boston College', 'June 19–28, 1967'], '1968', 
     ['Robert L. Carovillano', 'John F. McClay', 'Henry R. Radoski'],
     'E', None, 'AAA 02.12.11'),

    (11, ['Polar and Magnetospheric Substorms'], '1968', 
     ['Syun-Ichi Akasofu'],
     'A', None, ''),

    (12, ['Meteorite Research:', 'Proceedings of a Symposium on',
          'Meteorite Research Held in Vienna,',
          'Austria, 7–13 August 1968'], '1969', 
     ['Peter M. Millman'],
     'E', None, ''),

    (13, ['Mass Loss from Stars:', 'Proceedings of the Second Trieste',
          'Colloquim on Astrophysics, 12–17', 'September, 1969'], '1969', 
     ['Margherita Hack'],
     'E', None, 'AAA 01.12.23'),

    (14, ['Low-Frequency Waves and', 'Irregularities in the Ionosphere:',
          'Proceedings of the 2nd Esrin-Eslab',
          'Symposium, Held in Frascati, Italy,',
          '23–27 September, 1968'], '1969', 
     ['N. D’angelo'],
     'E', None, 'AAA 03.12.06'),

    (15, ['Space Engineering:', 'Proceedings of the Second',
          'International Conference on Space', 'Engineering'], '1970', 
     ['G. A. Partel'],
     'E', None, 'AAA 03.12.07'),

    (16, ['Manned Laboratories in Space:', 'Second International Orbital',
          'Laboratory Symposium'], '1969', 
     ['S. Fred Singer'],
     'E', None, 'AAA 03.12.05'),

    (17, ['Particles and Fields in the Magnetosphere',
          'Proceedings of a Symposium',
          'Organized by the Summer',
          'Advanced Study Institute, Held at',
          'the University of California, Santa',
          'Barbara, California, August 4–15,', '1969'], '1970', 
     ['B. M. McCormac'],
     'E', None, 'AAA 03.12.08'),

    (18, ['Experimental Astronomy'], '1970', 
     ['Jean-Claude Pecker'],
     'A', None, ''),

    (19, ['Intercorrelated Satellite', 'Observations Related to Solar',
          'Events:', 'Proceedings of the Third ESLAB/ESRIN',
          'Symposium Held in Noordwijk, The',
          'Netherlands, September 16–19, 1969'], '1970', 
     ['V. Manno', 'D. E. Page'],
     'E', None, 'AAA 04.12.19'),

    (20, ['Earthquake Displacement Fields and', 'the Rotation of the Earth:',
          'A NATO Advanced Study Institute', 'Conference Organized by the',
          'Department of Geophysics,',
          'University of Western Ontario, Canada',  '22 June – 28 June 1969'], '1970', 
     ['L. Mansinha', 'D. E. Smylie', 'A. E. Beck'],
     'E', None, 'AAA 04.12.25'),

    (21, ['Space Observatories'], '1970', 
     ['Jean-Claude Pecker'],
     'A', None, 'AAA 04.03.101'),

    (22, ['Structure and Evolution of the', 'Galaxy:',
          'Proceedings of the NATO Advanced', 'Study Institute Held in Athens,',
          'September 8–19, 1969'], '1971', 
     ['L. N. Mavridis'],
     'E', None, 'AAA 05.12.06'),

    (23, ['The Magellanic Clouds:', 'A European Southern Observatory',
          'Presentation: Principal Prospects,', 'Current Observational and',
          'Theoretical Approaches, and', 'Prospects for Future Research'], '1971', 
     ['André B. Muller'],
     'E', None, 'AAA 06.12.10'),

    (24, ['The Radiating Atmosphere:', 'Proceedings of a Symposium Organized by',
          'the Summer Advanced Study Institute,',
          'Held at Queens University', 'Kingston, Ontario, Aug 3-14, 1970'], '1971', 
     ['B. M. McCormac'],
     'E', None, 'AAA 06.12.21'),

    (25, ['Mesospheric Models and Related', 'Experiments:',
          'Proceedings of the Fourth', 'Esrin-Eslab Symposium Held in',
          'Frascati, Italy, 6–10 July, 1970'], '1971', 
     ['G. Fiocco'],
     'E', None, 'AAA 06.12.24'),

    (26, ['Selected Exercises in Galactic', 'Astronomy'], '1971', 
     ['I. Atanasijević'],
     'A', None, 'AAA 06.03.25'),

    (27, ['Physics of the Solar Coronae:', 'Proceedings of the NATO Advanced',
          'Study Institute on the Physics', 'of the Solar Coronae',
          'Held in Cavouri-Vouliagmeni,', 'Athens, Greece'
          '6-17 September 1970'], '1971', 
     ['C. J. Macris'],
     'E', None, 'AAA 07.12.11'),

    (28, ['The Environment of the Earth'], '1971', 
     ['Francis Delobeau'],
     'A', None, 'AAA 07.03.02'),

    # Volume 29 was published in four parts AAA 07.12.12-15
    # AAA 07.12.16 is the listing for all four volumes
    (29, ['Solar-Terrestrial Physics/1970:', 'Proceedings of the International',
          'Symposium on Solar-Terrestrial',
          'Physics Held in Leningrad, U.S.S.R.,', '12–-19 May 1970'], '1972', 
     ['C. de Jager', 'E. R. Dyer'],
     'E', None, 'AAA 07.12.16'),

    (30, ['Infrared Detection Techniques for', 'Space Research:',
          'Proceedings of the Fifth Eslab/Esrin',
          'Symposium Held in Noordwijk, The',
          'Netherlands, June 8–11, 1971'], '1972', 
     ['V. Manno', 'J. Ring'],
     'E', None, 'AAA 08.12.05'),

    (31, ['Gravitational N-Body Problem:', 'Proceedings of the IAU Colloquium',
          'No. 10 Held in Cambridge, England', 'August 12–15, 1970'], '1972', 
     ['Myron Lecar'],
     'E', None, 'AAA 07.12.04'),

    (32, ['Earth’s Magnetospheric Processes:',
          'Proceedings of a Symposium Organized', 'by the Summer Advanced Study',
          'Institute and Ninth ESRO Summer', 'School, Held in Cortina, Italy,',
          'August 30 –-- September 10, 1971'], '1972', 
     ['B. M. McCormac'],
     'E', None, 'AAA 08.12.09'),

    (33, ['Maps of Lunar Hemispheres'], '1972', 
     ['Antonín Rükl'],
     'A', None, ''),

    (34, ['Introduction to the Physics of', 'Stellar Interiors'], '1973', 
     ['V. Kourganoff'],
     'A', None, 'AAA 09.03.74'),

    (35, ['Physics and Chemistry of Upper', 'Atmosphere:',
          'Proceedings of a Symposium Organized',
          'by the Summer Advanced Study',
          'Institute, Held at the University of',
          'Orléans, France, July 31 – August', '11, 1972'], '1973', 
     ['B. M. McCormac'],
     'E', None, ''),

    (36, ['Variable Stars in Globular Clusters', 'and in Related Systems:',
          'Proceedings of the IAU Colloquium',
          'No. 21 Held at the University of', 'Toronto, Toronto, Canada August',
          '29–31, 1972'], '1973', 
     ['J. D. Fernie'],
     'E', None, 'AAA 10.12.06'),

    (37, ['Photon and Particle Interactions', 'with Surfaces in Space:',
          'Proceedings of the 6th Eslab', 'Symposium, Held at Noordwijk,',
          'The Netherlands, 26–29 September, 1972'], '1973', 
     ['R. J. L. Grard'],
     'E', None, 'AAA 10.12.33'),

    (38, ['Relativity, Astrophysics and', 'Cosmology:',
          'Proceedings of the Summer School',
          'Held, 14–26 August, 1972 at the',
          'Banff Centre, Banff, Alberta'], '1973', 
     ['Werner Israel'],
     'E', None, 'AAA 10.12.19'),

    (39, ['Recent Advances in Dynamical', 'Astronomy:',
          'Proceedings of the NATO Advanced', 'Study Institute in Dynamical',
          'Astronomy Held in Cortina D’Ampezzo,', 'Italy, August 9–21, 1972'],
     '1973', 
     ['B. D. Tapley', 'V. Szebehely'],
     'E', None, 'AAA 10.12.20'),

    (40, ['Cosmochemistry:', 'Proceedings of the Symposium on',
          'Cosmochemistry, Held at the', 'Smithsonian Astrophysical',
          'Observatory, Cambridge, Mass.,', ' August 14–16, 1972'], '1973', 
     ['A. G. W. Cameron'],
     'E', None, 'AAA 10.12.35'),

    (41, ['Introduction to Astronomical', 'Photometry'], '1974', 
     ['M. Golay'],
     'A', None, 'AAA 14.03.148'),

    (42, ['Correlated Interplanetary and', 'Magnetospheric Observations:',
          'Proceedings of the Seventh ESLAB', 'Symposium Held in Saulgau, W.',
          'Germany, 22–25 May , 1973'], '1974', 
     ['D. Edgar Page'],
     'E', None, 'AAA 11.12.16'),

    (43, ['X-Ray Astronomy'], '1974', 
     ['Riccardo Giacconi', 'Herbert Gursky'],
     'E', None, 'AAA 12.03.13'),

    (44, ['Magnetospheric Physics:', 'Proceedings of the Advanced Summer',
          'Institute Held in Sheffield, U.K.,', 'August 1973'], '1974', 
     ['B. M. McCormac'],
     'E', None, 'AAA 12.12.21'),

    (45, ['Supernovae and Supernova Remnants:',
          'Proceedings of the International',
          'Conference on Supernovae Held in',
          'Leece, Italy, May 7–11, 1973'], '1974', 
     ['Cristiano Batalli Cosmovici'],
     'E', None, 'AAA 11.12.15'),

    (46, ['Ionospheric Effects of Solar Flares'], '1974', 
     ['A. P. Mitra'],
     'A', None, 'AAA 12.03.14'),

    (47, ['Physics of Magnetospheric Substorms'], '1977', 
     ['Syun-Ichi Akasofu'],
     'A', '90-277-0748-0', 'AAA 19.03.18'),

    (48, ['Neutron Stars, Black Holes and', 'Binary X-Ray Sources'], '1975', 
     ['Herbert Gursky', 'Remo Ruffini'],
     'E', None, 'AAA 14.12.14'),

    (49, ['Catalog of Solar Particle Events', '1955–1969:',
          'Prepared under the Auspices of',
          'Working Group 2 of the Inter-Union',
          'Commission on Solar-Terrestrial', 'Physics'], '1975', 
     ['Z. Švestka', 'P. Simon'],
     'E', None, 'AAA 14.03.122'),

    (50, ['Mapping of the Moon: Past and Present'], '1974', 
     ['Zdeněk Kopal', 'Robert W. Carder'],
     'A', None, 'AAA 11.03.72'),

    (51, ['Atmospheres of Earth and the Planets:',
          'Proceedings of the Summer Advanced', 'Study Institute, Held at the',
          'University of Liège, Belgium,', 'July 29 – Ausgust 9, 1974'], '1975', 
     ['B. M. McCormac'],
     'E', None, ''),

    (52, ['The Magnetospheres of the Earth and', 'Jupiter:',
          'Proceedings of the Neil Brice', 'Memorial Symposium, Held in',
          'Frascati, May 28 – June 1, 1974'], '1975', 
     ['V. Formisano'],
     'E', None, ''),

    (53, ['The Solar Chromosphere and Corona:', 'Quiet Sun'], '1976', 
     ['R. Grant Athay'],
     'A', '90-277-0244-6', 'AAA 17.03.16'),

    (54, ['Image Processing Techniques in', 'Astronomy:',
          'Proceedings of a Conference Held in',
          'Utrecht on March 25–27, 1975'], '1975', 
     ['C. De Jager', 'H. Nieuwenhuijzen'],
     'E', None, 'AAA 14.12.41'),

    (55, ['Solid State Astrophysics:', 'Proceedings of a Symposium Held at',
          'the University College, Cardiff, Wales', '9–12 July 1974'], '1976', 
     ['N. C. Wickramasinghe', 'D. J. Morgan'],
     'E', None, 'AAA 17.12.01'),

    (56, ['Detection and Spectrometry of Faint', 'Light'], '1976', 
     ['John Meaburn'],
     'A', None, ''),

    (57, ['The Scientific Satellite Programme', 'during the International',
          'Magnetospheric Study:', 'Proceedings of the 10th ESLAB',
          'Symposium, Held at Vienna, Austria,', '10–13 June 1975'], '1976', 
     ['K. Knott', 'B. Battrick'],
     'E', None, 'AAA 17.12.02'),

    (58, ['Magnetospheric Particles and Fields:',
          'Proceedings of the Summer Advanced',
          'Study School, Held in Graz, Austria,', 'August 4–15, 1975'], '1976', 
     ['B. M. McCormac'],
     'E', '90-227-0702-2', 'AAA 18.12.32'),

    (59, ['Spallation Nuclear Reactions and', 'their Applications'], '1976', 
     ['B. S. P. Shen', 'M. Merker'],
     'E', '90-277-0746-4', 'AAA 18.12.33'),

    (60, ['Multiple Periodic Variable Stars:',
          'Proceedings of the International',
          'Astronomical Union Colloquium No. 29,',
          'Held at Budapest, Hungary', '1--5 September 1975'], '1976', 
     ['Walter S. Fitch'],
     'E', '90-277-0766-9', 'AAA 18.12.67'),

    (61, ['Atmospheric Physics from Spacelab:', 'Proceedings of the 11th ESLAB',
          'Symposium, Organized by the Space',
          'Science Department of the European',
          'Space Agency, Held at Frascati,', 'Italy, 11–14 May 1976'], '1976', 
     ['J. J. Burger', 'A. Pedersen', 'B. Battrick'],
     'E', '90-277-0768-5', 'AAA 18.12.23'),

    (62, ['Scientific Applications of Lunar', 'Laser Ranging:',
          'Proceedings of a Symposium Held in',
          'Austin, Tex., U.S.A.,', '8–-10 June,', '1976'], '1977', 
     ['J. Derral Mulholland', 'Creighton A. Burk', 'Eric C. Silverberg'],
     'E', '90-277-0790-1', 'AAA 20.12.12'),

    (63, ['Infrared and Submillimeter', 'Astronomy:',
          'Proceedings of a Symposium Held in',
          'Philadephia, Penn., U.S.A.,', 'June 8–10, 1976'], '1977', 
     ['Giovanni G. Fazio'],
     'E', '90-277-0791-X', 'AAA 19.12.03'),

    (64, ['Compilation, Critical Evaluation and',
          'Distribution of Stellar Data:',
          'Proceedings fo the International',
          'Astronomical Union Colloquium No. 35,',
          'held at Strasbourg, France,', '19–21 August, 1976'], '1977', 
     ['C. Jaschek', 'G. A. Wilkins'],
     'E', '90-277-0792-8', 'AAA 19.12.09'),

    (65, ['Novae and Related Stars:', 'Proceedings of an International',
          'Conference Held by the Institut',
          'D’Astrophysique, Paris, France,', '7 to 9 September 1976'], '1977', 
     ['M. Friedjung'],
     'E', '90-277-0793-6', 'AAA 19.12.01'),

    (66, ['Supernovae:', 'Proceedings of a Special IAU Session',
          'on Supernovae Held on September 1, 1976', 'in Grenoble, France'], '1977', 
     ['David N. Schramm'],
     'E', '90-277-0806-1', 'AAA 19.12.02'),

    (67, ['CNO Isotopes in Astrophysics:',
          'Proceedings of a Special IAU Session',
          'Held on August 30, 1976, in', 'Grenoble, France'], '1977', 
     ['Jean Audouze'],
     'E', '90-277-0807-X', 'AAA 19.12.14'),

    (68, ['Dynamics of Close Binary Systems'], '1978', 
     ['Zdeněk Kopal'],
     'A', '90-277-0820-7', 'AAA 22.03.78'),

    (69, ['Illustrated Glossary for Solar and', 'Solar-Terrestrial Physics'], '1977', 
     ['Dr. A. Bruzek', 'Dr. C. J. Durrant'],
     'E', '90-277-0825-8', 'AAA 20.03.22'),

    (70, ['Topics in Interstellar Matter:',
          'Invited Reviews Given for Commission 34',
          '(Interstellar Matter), of the',
          'International Astronomical Union, at',
          'the Sixteenth General Assembly of',
          'IAU, Grenoble, August 1976'], '1977', 
     ['Hugo Van Woerden'],
     'E', '90-277-0835-5', 'AAA 20.12.11'),

    (71, ['Study of travelling interplanetary', 'phenomena 1977',
          'Proceedings of the L.~D. de Feiter', 'Memorial Symposium held in'
           ' Tel Aviv, Israel, June 7--10, 1977'], '1977', 
     ['M. A. Shea', 'D. F. Smart', 'S. T. Wu'],
     'E', '90-277-0860-6', 'AAA 20.12.42'),

    (72, ['Dynamics of Planets and Satellites', 'and Theories of Their Motion:',
          'Proceedings of the 41st Colloquium',
          'of the International Astronomical',
          'Union Held in Cambridge, England,', '17–19 August 1976'], '1978', 
     ['Victor Szebehely'],
     'E', '90-277-0869-X', 'AAA 21.12.20'),

    (73, ['Spacecraft Attitude Determination', 'and Control'], '1978', 
     ['James R. Wertz'],
     'E', '90-277-0959-9', 'AAA 25.03.06'),

    (74, ['Wave Instabilities in Space Plasmas:',
          'Proceedings of a Symposium Organized',
          'within the XIXth URSI General',
          'Assembly Held in Helsinki, Finland,',
          'July 31 -- August 8, 1978'], '1979', 
     ['Peter J. Palmadesso', 'Konstantinos Papadopoulos'],
     'E', '90-277-1028-7', 'AAA 26.12.20'),

    (75, ['Stars and Star Systems:', 'Proceedings of the Fourth European',
          'Regional Meeting in Astronomy Held', 'in Uppsala, Sweden,',
          '7–12 August, 1978'], '1979', 
     ['Bengt E. Westerlund'],
     'E', '90-277-0983-1', 'AAA 25.12.45'),

    (76, ['Image Formation from Coherence', 'Functions in Astronomy:',
          'Proceedings of the IAU Colloquium', 'No.49 on the Formation of Images',
          'from Spatial Coherence Functions in', 'Astronomy, Held in Groningen,',
          'The Netherlands, 10–12 August 1978'], '1979', 
     ['Cornelis Van Schooneveld'],
     'E', '90-277-0987-4', 'AAA 25.12.46'),

    (77, ['Language of the Stars:', 'A Discourse on the Theory of the',
          'Light Changes of Eclipsing Variables'], '1979 *', 
     ['Zdeněk Kopal'],
     'A', '90-277-1001-5', 'AAA 26.03.75'),

    (78, ['Dynamics of the Magnetosphere:', 'Proceedings of the A.G.U. Chapman',
          'Conference ‘Magnetospheric Substorms', 'and Related Plasma Processes’ held',
          'at Los Alamos Scientific Laboratory,', 'Los Alamos, N.M, U.S.A.', 'October 9–13, 1978'], '1980', 
     ['S.-I. Akasofu'],
     'E', '90-277-1052-X', 'AAA 27.12.02'),

    (79, ['Gravity, Particles, and', 'Astrophysics:', 'A Review of Modern Theories of',
          'Gravity and G-variabilty, and their', 'Relation to Elementary Particle',
          'Physics and Astrophysics'], '1980', 
     ['Paul S. Wesson'],
     'E', '90-277-1083-X', 'AAA 28.03.111'),

    (80, ['Radio Recombination Lines:', 'Proceedings of a Workshop Held in',
          'Ottawa, Ontario, Canada,', 'August 24–25, 1979'], '1980', 
     ['P. A. Shaver'],
     'E', '90-277-1103-8', 'AAA 27.12.05'),

    (81, ['Astrophysics from Spacelab'], '1980', 
     ['Pier Luigi Bernacca', 'Remo Ruffini'],
     'E', '90-277-1064-3', 'AAA 27.12.50'),

    (82, ['Cosmic Plasma'], '1981', 
     ['Hannes Alfvén'],
     'A', '90-277-1151-8', 'AAA 29.03.17'),

    (83, ['Strategies for the Search for Life', 'in the Universe:',
          'A Joint Session of Commissions 16,', '40, and 44, Held in Montreal,',
          'Canada, During the IAU General', 'Assembly, 15 and 16 August, 1979'],
     '1980', 
     ['Michael D. Papagiannis'],
     'E', '90-277-1181-X', 'AAA 28.12.52'),

    (84, ['Relation Between Laboratory and', 'Space Plasmas:',
          'Proceedings of the International', 'Workshop held at Gakushi-Kaikan',
          '(University Alumni Association),', 'Tokyo, Japan, April 14–15, 1980'],
     '1981', 
     ['Hiroshi Kikuchi'],
     'E', '90-277-1248-4', 'AAA 29.12.49'),

    (85, ['Stellar Paths:', 'Photographic Astrometry with',
          'Long-Focus Instruments'], '1981', 
     ['Peter Van De Kamp'],
     'A', None, ''),

    (86, ['Reference Coordinate Systems for', 'Earth Dynamics:',
          'Proceedings of the 56th colloquium',
          'of the International Astronomical',
          'Union Held in Warsaw, Poland,', 'September 8–12, 1980'], '1981', 
     ['E. M. Gaposchkin', 'B. Kołaczek'],
     'E', '90-277-1260-3', 'AAA 29.12.45'),

    (87, ['X-Ray Astronomy with the Einstein', 'Satellite:',
          'Proceedings of the High Energy',
          'Astrophysics Division of the', 'American Astronomical Society',
          'Meeting on X-Ray Astronomy held at',
          'the Harvard/Smithsonian Center for', 'Astrophysics, Cambridge,',
          'Massachusetts, U.S.A.,', 'January 28–30, 1980'], '1981', 
     ['Riccardo Giacconi'],
     'E', '90-277-1261-1', 'AAA 29.12.55'),

    (88, ['Physical Processes in Red Giants:',
          'Proceedings of the Second Workshop,',
          'Held in Ettore Majorana Centre for',
          'Scientific Culture, Advanced School',
          'of Astronomy, in Erice, Sicily,', 'Italy, September 3–13, 1980'],
     '1981', 
     ['Icko Iben Jr.', 'Alvio Renzini'],
     'E', '90-277-1284-0', 'AAA 29.12.56'),

    (89, ['Effects of Mass Loss on Stellar', 'Evolution:',
          'IAU Colloquium no. 59 Held in',
          'Miramare, Trieste, Italy,', 'September 15–19, 1980'], '1981', 
     ['C. Chiosi', 'R. Stalio'],
     'E', None, ''),

    (90, ['The Orion Complex: A Case Study of', 'Interstellar Matter'], '1982', 
     ['C. Goudis'],
     'A', None, ''),

    (91, ['Investigating the Universe:', 'Papers presented to Zdeněk Kopal on',
          'the occasion of his retirement,', 'September 1981'], '1981', 
     ['F. D. Kahn'],
     'E', '90-277-1325-1', 'AAA 30.03.14'),

    (92, ['Instrumentation for Astronomy with', 'Large Optical Telescopes:',
          'Proceedings of IAU Colloquium No.', '67, Held at Zelenshikskaya,',
          'U.S.S.R., 8–10 September, 1981'], '1982', 
     ['Colin M. Humpfries'],
     'E', None, ''),

    (93, ['Regions of Recent Star Formation:', 'Proceedings of the Symposium on',
          '“Neutral Clouds near HII Regions ---',
          'Dynamics and Photochemistry”, Held',
          'in Penticton, British Columbia,', 'June 24–26, 1981'], '1982', 
     ['R. S. Roger', 'Peter E. Dewdney'],
     'E', None, ''),

    (94, ['High-Precision Earth Rotation and', 'Earth-Moon Dynamics:',
          'Lunar Distance and Related', 'Observations'], '1982', 
     ['O. Calame'],
     'E', None, ''),

    (95, ['The Nature of Symbiotic Stars:', 'Proceedings of IAU Colloquium No. 70',
          'Held at the Observatoire De Haute', 'Provence, 26–28 August 1981'], '1982', 
     ['Michael Friedjung', 'Roberto Viotti'],
     'E', None, ''),

    (96, ['Sun and Planetary System:', 'Proceedings of the Sixth European',
          'Regional Meeting in Astronomy, Held',
          'in Dubrovnik, Yugoslavia,', '19--23 October 1981'], '1982', 
     ['W. Fricke', 'G. Teleki'],
     'E', None, ''),

    (97, ['Automated Data Retrieval in', 'Astronomy:',
          'Proceedings of the 64th Colloquium',
          'of the International Astronomical',
          'Union Held in Strasbourg, France,', 'July 7–10, 1981'], '1982', 
     ['Carlos Jaschek', 'W. Heintz'],
     'E', None, ''),

    (98, ['Binary and Multiple Stars as Tracers', 'of Stellar Evolution:',
          'Proceedings of the 69th Colloquium',
          'of the International Astronomical', 'Union, held im Bamberg, F.R.G.,',
          'August 31 – September 3, 1981'], '1982', 
     ['Zdenék Kopal', 'Jürgen Rahe'],
     'E', None, ''),

    (99, ['Progress in Cosmology:', 'Proceedings of the Oxford',
          'International Symposium Held in', 'Christ Church, Oxford,',
          'September 14–18, 1981'], '1982', 
     ['A. W. Wolfendale'],
     'E', None, ''),

    (100, ['Kinematics, Dynamics and Structure', 'of the Milky Way:',
           'Proceedings of a Workshop on ‘The', 'Milky Way” Held in Vancouver,',
           'Canada, May 17–19, 1982'], '1983', 
     ['W. L. H. Shuter'],
     'E', None, ''),

    (101, ['Cataclysmic Variables and Related', 'Objects:',
           'Proceedings of the 72nd Colloquium',
           'of International Astronomical Union',
           'Held in Haifa, Israel, August 9–13,', '1982'], '1983', 
     ['Mario Livio', 'Giora Shaviv'],
     'E', None, ''),

    (102, ['Activity in Red-Dwarf Stars:', 'Proceedings of the 71st Colloquium',
           'of the International Astronomical',
           'Union Held in Catania, Italy,', 'August 10–13, 1982'], '1983', 
     ['Patrick B. Byrne', 'Marcello Rodonò'],
     'E', None, ''),

    (103, ['Astrophysical Jets:', 'Proceedings of an International',
           'Workshop held in Torino, Italy,', 'October 7–9, 1982'], '1983', 
     ['A. Ferrari', 'A. G. Pacholczyk'],
     'E', None, ''),

    (104, ['Solar-Terrestrial Physics:', 'Principles and Theoretical',
           'Foundations Based Upon the', 'Proceedings of the Theory Institute',
           'Held at Boston College,', 'August 9–26, 1982'], '1983', 
     ['R. L. Carovillano', 'J. M. Forbes'],
     'E', None, ''),

    (105, ['Surveys of the Southern Galaxy:',
           'Proceedings of a Workshop Held at', 'the Leiden Observatory,',
           'The Netherlands, August 4–6, 1982'], '1983', 
     ['W. B. Burton', 'F. P. Israel'],
     'E', None, ''),

    (106, ['Dynamical Trapping and Evolution in', 'the Solar System:',
           'Proceedings of the 74th Colloquium',
           'of the International Astronomical',
           'Union Held in Gerakini, Chalkidiki,',
           'Greece,', '30 August – 2 September, 1982'], '1983', 
     ['Vassilis V. Markellos', 'Yoshihide Kozai'],
     'E', None, ''),

    (107, ['Planetary Nebulae:', 'A Study of Late Stages of Stellar',
           'Evolution'], '1983', 
     ['Stuart Robert Pottasch'],
     'A', None, ''),

    (108, ['Galactic and Extragalactic Infrared', 'Spectroscopy:',
           'Proceedings of the XVIth ESLAB',
           'Symposium, held in Toledo, Spain,', 'December 6–8, 1982'], '1984', 
     ['M. F. Kessler', 'J. P. Phillips'],
     'E', None, ''),

    (109, ['Stellar Nucleosynthesis:', 'Proceedings of the Third Workshop of',
           'the Advanced School of Astronomy of',
           'the Ettore Majorana Centre for',
           'Scientific Culture, Erice, Italy,', 'May 11–21, 1983'], '1984', 
     ['Cesare Chiosi', 'Alvio Renzini'],
     'E', None, ''),

    (110, ['Astronomy with Schmidt-Type', 'Telescopes:',
           'Proceedings of the 78th Colloquium',
           'of the International Astronomical',
           'Union, Asiago, Italy,', 'August 30 – September 2, 1983'], '1984', 
     ['Massimo Capaccioli'],
     'E', None, ''),

    (111, ['Clusters and Groups of Galaxies:', 'International Meeting Held in',
           'Trieste, Italy,', 'September 13–16, 1983'], '1984', 
     ['F. Mardirossian', 'G. Giuricin', 'M. Mezzetti'],
     'E', None, ''),

    (112, ['Physics of Thermal Gaseous Nebulae:',
           'Physical Processes in Gaseous', 'Nebulae'], '1984', 
     ['Lawrence H. Aller'],
     'A', None, ''),

    (113, ['Cataclysmic Variables and Low-Mass',
           'X-Ray Binaries:', 'Proceedings of the 7th North',
           'American Workshop held in Cambridge,',
           'Massachusetts, U.S.A.,', 'January 12–15, 1983'], '1985', 
     ['Donald Q. Lamb', 'Joseph Patterson'],
     'E', None, ''),

    (114, ['Cool Stars with Excesses of Heavy', 'Elements:',
           'Proceedings of the Strasbourg',
           'Observatory Colloquium Held in',
           'Strasbourg, France, July 3–6, 1984'], '1985', 
     ['Mercedes Jaschek', 'Philip C. Keenan'],
     'E', None, ''),

    (115, ['Dynamics of Comets: Their Origin and', 'Evolution:',
           'Proceedings of the 83rd Colloquium',
           'of the International Astronomical',
           'Union, Held in Rome, Italy, 11–15', 'June 1984'], '1985', 
     ['Andrea Carusi', 'Giovanni B. Valsecchi'],
     'E', None, ''),

    (116, ['Radio Stars:', 'Proceedings of a Workshop on Stellar',
           'Continuum Radio Astronomy Held in',
           'Boulder, Colorado, U.S.A.,', '8–10 August 1984'], '1985', 
     ['Robert M. Hjellming', 'David M. Gibson'],
     'E', None, ''),

    (117, ['Mass Loss from Red Giants:', 'Proceedings of a Conference held at',
           'the University of California at Los',
           'Angeles, U.S.A., June 20–21, 1984'], '1985', 
     ['Mark Morris', 'Ben Zuckerman'],
     'E', None, ''),

    (118, ['Early History of Cosmic Ray Studies:',
           'Personal Reminiscences with Old', 'Photographs'], '1985', 
     ['Yataro Sekido', 'Harry Elliot'],
     'E', None, ''),

    (119, ['Properties and Interactions of', 'Interplanetary Dust:',
           'Proceedings of the 85th Colloquium', 'of the International Astronomical',
           'Union, Marseille, France,', 'July 9–12, 1984'], '1985', 
     ['R. H. Giese', 'P. Lamy'],
     'E', None, ''),

    (120, ['Birth and Evolution of Massive Stars', 'and Stellar Groups:',
           'Proceedings of a Symposium held in', 'Dwingeloo, The Netherlands,',
           '24–25 September 1984'], '1985', 
     ['Wilfried Boland', 'Hugo van Woerden'],
     'E', None, ''),

    (121, ['Structure and Evolution of', 'Active Galactic Nuclei'], '1986', 
     ['G. Giuricin', 'F. Mardirossian', 'M. Mezzetti', 'M. Ramella'],
     'E', '978-90-277-2155-6', ''),

    (122, ['Spectral Evolution of Galaxies:', 'Proceedings of the Fourth Workshop',
           'of the Advanced School of Astronomy', 'of the ‘Ettore Majorana” Centre for',
           'Scientific Culture, Erice, Italy,', 'March 12–22, 1985'], '1986', 
     ['Cesare Chiosi', 'Alvio Renzini'],
     'E', None, ''),

    (123, ['The Sun and the Heliosphere in Three', 'Dimensions:',
           'Proceedings of the XIXth ESLAB', 'Symposium, held in Les Diablerets,',
           'Switzerland, 4–6 June 1985'], '1986', 
     ['R. G. Marsden'],
     'E', None, ''),

    (124, ['Light on Dark Matter:', 'Proceedings of the First IRAS',
           'Conference, Held in Noordwijk, the', 'Netherlands, 10–14 June 1985'], '1986', 
     ['Frank P. Israel'],
     'E', None, ''),

    (125, ['Upper Main Sequence Stars with', 'Anomalous Abundances:',
           'Proceedings of th 90th Colloquium of', 'the International Astronomical',
           'Union, held in Crimea, U.S.S.R.,', 'May 13–19, 1985'], '1986', 
     ['C. R. Cowley', 'M. M. Dworetsky', 'C. Mégessier'],
     'E', None, ''),

    (126, [], None, 
     [],
     None, None, ''),

    (127, ['Space Dynamics and Celestial', 'Mechanics:', 'Proceedings of the International',
           'Workshop, Delhi, India,', '14–16 November 1985'], '1986', 
     ['K. B. Bhatnagar'],
     'E', None, ''),

    (128, ['Hydrogen Deficient Stars and Related', 'Objects:',
           'Proceedings of the 87th Colloquium', 'of the International Astronomical',
           'Union Held at Mysore, India,', '10–15 November 1985'], '1986', 
     ['Kurt Hunger', 'Detlef Schönberner', 'N. Kameswara Rao'],
     'E', None, ''),

    (129, ['Exploring the Universe with the IUE', 'Satellite'], '1987', 
     ['Y. Kondo', 'W. Wamsteker', 'A. Boggess', 'M. Grewing', 'C. De Jager', 'A. L. Lane',
      'J. L. Linksy', 'R. Wilson'],
     'E', None, ''),

    (130, ['Jacobi Dynamics:', 'Many-Body Problem in Integral', 'Characteristics'], '1987', 
     ['V. I. Ferronsky', 'S. A. Denisik', 'S. V. Ferronsky'],
     'A', None, ''),

    (131, ['Multivariate Data Analysis'], '1987', 
     ['Fionn Murtagh', 'André Heck'],
     'A', None, ''),

    (132, ['Late Stages of Stellar Evolution:', 'Proceedings of the Workshop Held in',
           'Calgary, Canada, from 2–5 June, 1986'], '1987', 
     ['S. Kwok', 'S. R. Pottasch'],
     'E', None, ''),

    (133, ['Magnetic Fields of Galaxies'], '1988', 
     ['A. A. Ruzmaikin', 'A. M. Shukurov', 'D. D. Sokoloff'],
     'A', None, ''),

    (134, ['Interstellar Processes:', 'Proceedings of the Symposium on',
           'Interstellar Processes, Held in', 'Grand Teton National Park, July 1985'], '1987', 
     ['David J. Hollenbach', 'Harley A. Thronson Jr.'],
     'E', None, ''),

    (135, ['Planetary and Proto-Planetary', 'Nebulae: From IRAS to ISO:',
           'Proceedings of the Frascati Workshop', '1986, Vulcano Island,',
           'September 8–12, 1986'], '1987', 
     ['Andrea Preite Martinez'],
     'E', None, ''),

    (136, ['Instabilities in Luminous Early Type', 'Stars:',
           'Proceedings of a workshop in Honour', 'of Professor Cees De Jager on the',
           'Occasion of his 65th Birthday held', 'in Lunteren, The Netherlands,',
           '21–24 April 1986'], '1987', 
     ['Henny J. G. L. M. Lamers', 'Camiel W. H. De Loore'],
     'E', None, ''),

    (137, ['The Internal Solar Angular Velocity:', 'Theory, Observations and',
           'Relationship to Solar Magnetic', 'Fields'], '1987', 
     ['Bernard R. Durney', 'Sabatino Sofia'],
     'E', None, ''),

    (138, ['Physics of Formation of FeII Lines', 'Outside of LTE:',
           'Proceedings of the 94th Colloquium', 'of the International Astronomical',
           'Union Held in Anacapri, Capri', 'Islands, Italy, 4–8 July 1986'], '1988', 
     ['Roberto Viotto', 'Alberto Vittone', 'Michael Friedjung'],
     'E', None, ''),

    (139, ['Resolute and Undertaking Characters:', 'The Lives of Wilhelm and Otto Struve'], '1988', 
     ['Alan H. Batten'],
     'A', None, ''),

    (140, ['The Few Body Problem:', 'Proceedings of the 96th Colloquium',
           'of the International Astronomical', 'Union Held in Turky, Finland,',
           'June 14–19, 1987'], '1988', 
     ['M. J. Valtonen'],
     'E', None, ''),

    (141, ['Towards Understanding Galaxies at', 'Large Redshift:',
           'Proceedings of the Fifth Workshop of', 'the Advanced School of Astronomy of',
           'the Ettore Majorana Centre for', 'Scientific Culture, Erice, Italy,',
           'Juni 1–10, 1987'], '1988', 
     ['Richard G. Kron', 'Alvio Renzini'],
     'E', None, ''),

    (142, ['Mass Outflows from Stars and', 'Galactic Nuclei:',
           'Proceedings of the Second Torino', 'Workshop, Held in Torino, Italy,',
           'May, 4–8, 1987'], '1988', 
     ['Luciana Bianchi', 'Roberto Gilmozzi'],
     'E', None, ''),

    (143, ['Activity in Cool Star Envelopes:', 'Proceedings of the Midnight Sun',
           'Conference Held in Tromsø, Norway,', 'July 1–8, 1987'], '1988', 
     ['O. Havnes', 'B. R. Pettersen', 'J. H. M. M. Schmitt', 'J. E. Solheim'],
     'E', None, ''),

    (144, ['Bioastronomy — The Next Steps,', 'Proceedings of the 99th Colloquium',
           'of the International Astronomical', 'Union held in Balaton, Hungary,',
           'June 22–27, 1987'], '1988', 
     ['George Marx'],
     'E', None, ''),

    (145, ['The Symbiotic Phenomenon:', 'Proceedings of the 103rd Colloquium',
           'of the International Astronomical', 'Union, Held in Torun, Poland,',
           'August 18–20, 1987'], '1988', 
     ['Joanna Mikolajewska', 'Michael Friedjung', 'Scott J. Kenyon', 'Roberto Viotti'],
     'E', None, ''),

    (146, ['Rate Coefficients in Astrochemistry:', 'Proceedings of a Conference held in',
           'Umis, Manchester, U.K.,', 'September 21–24, 1987'], '1988', 
     ['T. J. Millar', 'D. A. Williams'],
     'E', None, ''),

    (147, ['Millimetre and Submillimetre', 'Astronomy:', 'Lectures Presented at a Summer',
           'School Held in Stirling, Scotland,', 'June 21–27, 1987'], '1988', 
     ['R. D. Wolstencroft', 'W. B. Burton'],
     'E', None, ''),

    (148, ['Pulsation and Mass Loss in Stars:', 'Proceedings of a Workshop Held in',
           'Trieste, Italy,', 'September 14–18, 1987'], '1988', 
     ['R. Stalio', 'L. A. Willson'],
     'E', None, ''),

    (149, ['Experiments on Cosmic Dust', 'Analogues:', 'Proceedings of the Seconds',
           'International Workshop of the', 'Astronomical Observatory of',
           'Capodimonte (QAC 2), held at Capri,', 'Italy, September 8–12, 1987'], '1988', 
     ['Ezio Bussoletti', 'Carlo Fusco', 'Giuseppe Longo'],
     'E', None, ''),

    (150, ['Dynamics and Structure of Quiescent', 'Solar Prominences'], '1989', 
     ['E. R. Priest'],
     'E', None, ''),

    (151, ['Large Scale Structure and Motions in', 'the Universe:',
           'Proceedings of an International', 'Meeting Held in Trieste, Italy,',
           'April 6–9, 1988'], '1989', 
     ['M. Mezzetti', 'G. Giuricin', 'F. Mardirossian', 'M. Ramella'],
     'E', None, ''),

    (152, ['The Roche Problem:', 'And its Significance for Double-Star', 'Astronomy'], '1989', 
     ['Zdenĕk Kopal'],
     'A', None, ''),

    (153, ['Energetic Phenomena on the Sun'], '1989', 
     ['M. R. Kundu', 'B. Woodgate', 'E. J. Schmahl'],
     'E', None, ''),

    (154, ['Reference Frames:', 'In Astronomy and Geophysics'], '1989', 
     ['Dr Jean Kovalevsky', 'Prof Ivan I. Mueller', 'Dr Barbara Kolaczek'],
     'E', None, ''),

    (155, ['Astronomy, Cosmology and Fundamental', 'Physics:',
           'Proceedings of the Third ESO-CERN', 'Symposium, Held in Bologna, Palazzo'
           , 'Re Enzo, May 16–20, 1988'], '1989', 
     ['Michele Caffo', 'Roberto Fanti', 'Giorgio Giacomelli', 'Alvio Renzini'],
     'E', None, ''),

    (156, ['Accretion Disks and Magnetic Fields', 'in Astrophysics:',
           'Proceedings of the European Physical', 'Society Study Conference, Held in',
           'Noto (Sicily), Italy, June 16–21,', '1988'], '1989', 
     ['G. Belvedere'],
     'E', None, ''),

    (157, ['Physics of Luminous Blue Variables:', 'Proceedings of the 113th Colloquium',
           'of the International Astronomical', 'Union, Held at Val Morin, Quebec',
           'Province, Canada, August 15–18, 1988'], '1989', 
     ['Kris Davidson', 'A. F. J. Moffat', 'H. J. G. L. M. Lamers'],
     'E', None, ''),

    (158, ['Submillimetre Astronomy:', 'Proceedings of the Kona Symposium on',
           'Millimetre and Submillimetre', 'Astronomy, Held at Kona, Hawaii,',
           'October 3–6, 1988'], '1990', 
     ['Graeme D. Watt', 'Adrian S.'],
     'E', None, ''),

    (159, ['Inside the Sun:', 'Proceedings of the 121st Colloquium',
           'of the International Astronomical', 'Union, Held at Versailles, France,',
           'May 22–26, 1989'], '1990', 
     ['Gabrielle Berthomieu', 'Michel Cribier'],
     'E', None, ''),

    (160, ['Windows on Galaxies:', 'Proceedings of the Sixth Workshop of',
           'the Advanced School of Astronomy of', 'the Ettore Majorana Centre for',
           'Scientific Culture, Erice, Italy,', 'May 21–31, 1989'], '1990', 
     ['Giuseppina Fabbiano', 'John S. Gallagher', 'Alvio Renzini'],
     'E', None, ''),

    (161, ['The Interstellar Medium in Galaxies'], '1990', 
     ['Harley A. Thronson Jr.', 'J. Michael Shull'],
     'E', None, ''),

    (162, ['Physical Processes in Fragmentation', 'and Star Formation:',
           'Proceedings of the Workshop on', '‘Physical Processes in Fragmentation',
           'and Star Formation’, Held in', 'Monteporzio Catone,(Rome), Italy,',
           'June 5–11, 1989'], '1990', 
     ['Roberto Capuzzo-Dolcetta', 'Cesare Chiosi', 'Alberto di Fazio'],
     'E', None, ''),

    (163, ['Radio Recombination Lines: 25 Years', 'of Investigation:',
           'Proceedings of the 125th Colloquium', 'of the International Astronomical',
           'Union, Held in Puschino, U.S.S.R.,', 'September 11–16, 1989'], '1990', 
     ['M. A. Gordon', 'R. L. Sorochenko'],
     'E', None, ''),

    (164, ['The Cosmic Microwave Background: 25', 'Years Later:',
           'Proceedings of the Meeting on ‘The', 'Cosmic Microwave Background: 25',
           'Years Later’, Held in L’Aquila,', 'Italy, June 19–23, 1989'], '1990', 
     ['N. Mandolesi', 'N. Vittorio'],
     'E', None, ''),

    (165, ['Dusty Objects in the Universe:', 'Proceedings of the Fourth',
           'International Workshop of the', 'Astronomical Observatory of',
           'Capodimonte (OAC 4), Held in Capri,', 'Italy, September 8–13, 1989'], '1990', 
     ['E. Bussoletti', 'A. A. Vittone'],
     'E', None, ''),

    (166, ['Observatories in Earth Orbit and', 'Beyond:', 'Proceedings of the 123rd Colloquium',
           'of the International Astronomical', 'Union, Held in Greenbelt, Maryland,',
           'U.S.A., April 24–27, 1990'], '1990', 
     ['Y. Kondo'],
     'E', None, ''),

    (167, ['Comets in the Post-Halley Era:', 'Volume 1:', 'In Part Based on reviews Presented',
           'at the 121st Colloquium of the', 'International Astronomical Union,',
           'Held in Bamberg, Germany, April', '24–28, 1989'], '1991', 
     ['R. L. Newburn Jr.', 'M. Neugebauer', 'J. Rahe'],
     'E', None, ''),

    (168, ['The Theory of Cosmic Grains'], '1991', 
     ['F. Hoyle', 'N. C. Wickramasinghe'],
     'A', None, ''),

    (169, ['Primordial Nucleosynthesis and', 'Evolution of Early Universe:',
           'Proceedings of the International', 'Conference ‘Primordial',
           'Nucleosynthesis and Evolution of the', 'Early Universe”, Held in Tokyo,',
           'Japan, September 4–8, 1990'], '1991', 
     ['K. Sato', 'J. Audouze'],
     'E', None, ''),

    (170, ['Astronomical Masers'], '1992', 
     ['Moshe Elitzur'],
     'A', None, ''),

    (171, ['Databases and On-line Data in', 'Astronomy'], '1991', 
     ['Miguel A. Albrecht', 'Daniel Egret'],
     'E', None, ''),

    (172, ['Physical Processes in Solar Flares'], '1992', 
     ['Boris V. Somov'],
     'A', None, ''),

    (173, ['Origin and Evolution of', 'Interplanetary Dust:',
           'Proceedings of the 126th Colloquium', 'of the International Astrononmical',
           'Union, Held in Kyoto, Japan,', 'August 27–30, 1990'], '1991', 
     ['A. C. Levasseur-Regourd', 'H. Hasegawa'],
     'E', None, ''),

    (174, ['Digitised Optical Sky Surveys:', 'Proceedings of the Conference on',
           '“Digitised Optical Sky Surveys”,', 'Held in Edinburgh, Scotland,',
           '18–21 June 1991'], '1992', 
     ['H. T. MacGillivray', 'E. B. Thomson'],
     'E', None, ''),

    (175, ['Astronomical Photometry:', 'A Guide'], '1992', 
     ['Chr. Sterken', 'J. Manfroid'],
     'A', None, ''),

    (176, ['The Andromeda Galaxy'], '1992', 
     ['Paul Hodge'],
     'A', None, ''),

    (177, ['The Realm of Interacting Binary', 'Stars'], '1993', 
     ['J. Sahade', 'G. E. McCluskey Jr.', 'Y. Kondo'],
     'E', None, ''),

    (178, ['Morphological and Physical', 'Classification of Galaxies:',
           'Proceedings of the Fifth', 'International Workshop of the',
           'Osservatories Astronomico di', 'Capodimonite, Held in Sant’Agata Sui',
           'Due Golfi, Italy,', 'September 3–7, 1990'], '1992', 
     ['G. Longo', 'M. Capaccioli', 'G. Busarello'],
     'E', None, ''),

    (179, ['Structure and Evolution of Single', 'and Binary Stars'], '1992', 
     ['C. W. H. De Loore', 'C. Doom'],
     'A', None, ''),

    (180, ['The Center, Bulge, and Disk of the', 'Milky Way'], '1992', 
     ['Leo Blitz'],
     'E', None, ''),

    (181, [], None, 
     [],
     None, None, ''),

    (182, ['Intelligent Information Retrieval:', 'The Case of Astronomy and Related',
           'Space Sciences'], '1993', 
     ['A. Heck', 'F. Murtagh'],
     'E', None, ''),

    (183, ['Physics of Solar and Stellar', 'Coronae: G.S. Vaiana Memorial', 'Symposium:',
           'Proceedings of a Conference of the', 'International Astronomical Union,',
           'Held in Palermo, Italy,', '22–26 June, 1992'], '1993', 
     ['Jeffrey F. Linsky', 'Salvatore Serio'],
     'E', None, ''),

    (184, ['Plasma Astrophysics:', 'Kinetic Processes in Solar and', 'Stellar Coronae'], '1993', 
     ['Arnold Benz'],
     'A', None, ''),

    (185, ['Stability of Collisionless Stellar', 'Systems:', 'Mechanisms for the Dynamical',
           'Structure of Galaxies'], '1994', 
     ['P. L. Palmer'],
     'A', None, ''),

    (186, ['Stellar Jets and Bipolar Outflows:', 'Proceedings of the Sixth',
           'International Workshop of the', 'Astronomical Observatory of',
           'Capodimonte (OAC 6), Held at Capri,', 'Italy, September 18–21, 1991'], '1993', 
     ['L. Errico', 'A. A. Vittone'],
     'E', None, ''),

    (187, ['Frontiers of Space And Ground-Based', 'Astronomy:',
           'The Astrophysics of the 21st Century'], '1994', 
     ['W. Wamsteker', 'M. S. Longair', 'Y. Kondo'],
     'E', None, ''),

    (188, ['The Environment and Evolution of', 'Galaxies:', 'Proceedings of the Third Tetons',
           'Summer School Held in Grand Tetons',
           'National Park, Wyoming, U.S.A.,', 'July 1992'], '1993', 
     ['J. Michael Shull', 'Harley A. Thronson Jr.'],
     'E', None, ''),

    (189, ['Solar Magnetic Fields:', 'Polarized Radiation Diagnostics'], '1994', 
     ['Jan Olof Stenflo'],
     'A', None, ''),

    (190, ['Infrared Astronomy with Arrays:', 'The Next Generation'], '1994', 
     ['Ian S. McLean'],
     'E', None, ''),

    (191, ['Fundamentals of Cosmic', 'Electrodynamics'], '1994', 
     ['Boris V. Somov'],
     'A', None, ''),

    (192, [], None, 
     [],
     None, None, ''),

    (193, ['Dusty and Self-Gravitational Plasmas', 'in Space'], '1995', 
     ['Pavel Bliokh', 'Victor Sinitsin', 'Victoria Yaroshenko'],
     'A', None, ''),

    (194, [], None, 
     [],
     None, None, ''),

    (195, [], None, 
     [],
     None, None, ''),

    (196, [], None, 
     [],
     None, None, ''),

    (197, [], None, 
     [],
     None, None, ''),

    (198, ['Magnetic Fields of Celestial Bodies'], '1994', 
     ['Ye Shi-Hui'],
     'A', None, ''),

    (199, ['The Nature of Solar Prominences'], '1995', 
     ['Einar Tandberg-Hanssen'],
     'A', None, ''),

    (200, ['Polarization Spectroscopy of Ionized', 'Gases'], '1995', 
     ['S. A. Kazantsev', 'J.-C. Hénoux'],
     'A', None, ''),

    (201, ['Modulational Interactions in Plasmas'], '1995', 
     ['Sergey V. Vladimirov', 'Vadim N. Tsytovich', 'Sergey I. Popel', 'Fotekh Kh. Khakimov'],
     'A', None, ''),

    (202, ['The Diffuse Interstellar Bands'], '1995', 
     ['A. G. G. M. Tielens', 'T. P. Snow'],
     'E', None, ''),

    (203, ['Information \& On-Line Data in', 'Astronomy'], '1995', 
     ['Daniel Egret', 'Miguel A. Albrecht'],
     'E', None, ''),

    (204, ['Radiation in Astrophysical Plasmas'], '1996', 
     ['V. V. Zheleznyakov'],
     'A', None, ''),

    (205, ['Cataclysmic Variables:', 'Proceedings of the Conference held',
           'in Abano Terme, Italy,', '20--24 June 1994'], '1995', 
     ['A. Bianchini', 'M. Della Valle', 'M. Orio'],
     'E', None, ''),

    (206, ['Cold Gas at High Redshift:', 'Proceedings of a Workshop',
           'Celebrating the 25th Anniversary of', 'the Westerbork Synthesis Radio',
           'Telescope, held in Hoogeveen, The', 'Netherlands, August 28--30, 1995'], '1996', 
     ['M. N. Bremer', 'P. P. van der Werf', 'H. J. A. Röttgering', 'C. L. Carilli'],
     'E', None, ''),

    (207, ['The Westerbork Observatory,', 'Continuing Adventure in Radio', 'Astronomy'], '1996', 
     ['Ernst Raimond', 'René Genee'],
     'E', None, ''),

    (208, ['Cataclysmic Variables and Related', 'Objects:', 'Proceedings of the 158th Colloquium',
           'of the International Astronomical', 'Union, Held at Keele, United',
           'Kingdom, June 26--30 1995'], '1996', 
     ['A. Evans', 'Janet H. Wood'],
     'E', None, ''),

    (209, ['New Extragalactic Perspectives in', 'the New South Africa:',
           'Proceedings of the International', 'Conference on “Cold Dust and Galaxy',
           'Morphology" held in Johannesburg', 'South Africa January 22--26 1996'], '1996', 
     ['David L. BlockJ', '. Mayo Greenberg'],
     'E', None, ''),

    (210, ['The Impact of Large Scale Near-IR', 'Sky Surveys:',
           'Proceedings of a Workshop held at', 'Puerto de la Cruz, Tenerife (Spain),',
           '22--26 April, 1996'], '1997', 
     ['F. Garzón', 'N. Epchtein', 'A. Omont', 'B. Burton', 'P. Persi'],
     'E', None, ''),

    (211, [], None, 
     [],
     None, None, ''),

    (212, ['Wide-Field Spectroscopy:', 'Proceedings of the 2nd Conference of',
           'the Working Group of IAU Commission 9', 'on “Wide-Field Imaging” held in',
           'Athens, Greece, May 20--25, 1996'], '1997', 
     ['E. Kontizas', 'M. Kontizas', 'D. H. Morgan', 'G. P. Vettolani'],
     'E', None, ''),

    (213, ['The Letters and Papers of Jan', 'Hendrik Oort:', 'as Archived in the University',
           'Library, Leiden'], '1997', 
     ['J. K. Katgert-Merkelijn'],
     'A', None, ''),

    (214, ['White Dwarfs:', 'Proceedings of the 10th European',
           'Workshop on White Dwarfs, held in', 'Blanes, Spain, 17--21 June 1996'], '1997', 
     ['J. Isern', 'M. Hernanz', 'E. García-Berro'],
     'E', None, ''),

    (215, ['Infrared Space Interferometry:', 'Astrophysics \& the Study of',
           'Earth-Like Planets:', 'Proceedings of a Workshop held in',
           'Toledo, Spain, March 11--14, 1996'], '1997', 
     ['C. Eiroa', 'A. Alberdi', 'H. Thronson', 'T. De Graauw', 'C. J. Schalinski'],
     'E', None, ''),

    (216, ['Magnetohydrodynamics in',
           'Binary Stars'], '1997-08',
     ['C. G. Campbell'],
     'A', '0-7923-4606-8', ''),

    (217, ['Nonequilibrium Processes',
           'in the Planetary and Cometary',
           'Atmospheres'], '1997-09',
     ['Mikhail Ya. Marov', 'Valery I. Shematovich', 'Dmitry V. Bisikalo',
      'Jean-Claude Gérard'],
     'A', '0-7923-4686-6', ''),

    (218, ['Astronomical Time Series:', 'Proceedings of the Florence and',
           'George Wise Observatory 25th', 'Anniversary Symposium held in',
           'Tel-Aviv, Israel,', '30 December 1996 -- 1 January 1997'], '1997', 
     ['Dan Maoz', 'Amiel Sternberg', 'Elia M. Leibowitz'],
     'E', None, ''),

    (219, ['The Interstellar Medium in Galaxies'], '1997', 
     ['J. M. van der Hulst'],
     'E', None, ''),

    (220, ['The Three Galileos: The Man, the', 'Spacecraft, the Telescope:',
           'Proceedings of the Conference held', 'in Padova, Italy on January 7--10,', '1997'], '1998', 
     ['Cesare Barbieri', 'Jürgen H. Rahe', 'Torrence V. Johnson', 'Anita M. Sohus'],
     'E', None, ''),

    (221, ['An Atlas of Local Group Galaxies'], '2002', 
     ['Paul W. Hodge', 'Brooke P. Skelton', 'Joy Ashizawa'],
     'A', None, ''),

    (222, ['Remembering Edith Alice Müller'], '1998', 
     ['I. Appenzeller', 'Y. Chmielewski', 'J.-C. Pecker', 'R. De la Reza',
      'G. Tammann', 'P. Wayman'],
     'E', None, ''),

    (223, ['Visual Double Stars: Formation,', 'Dynamics and Evolutionary Tracks'], '1997', 
     ['J. A. Docobo', 'A. Elipe', 'H. McAlister'],
     'E', None, ''),

    (224, ['Electronic Publishing for Physics', 'and Astronomy'], '1997', 
     ['André Heck'],
     'E', None, ''),

    (225, ['SCORe ’96: Solar Convection and', 'Oscillations and their Relationship'], '1997', 
     ['F. P. Pijpers', 'J. Christensen-Dalsgaard', 'C. S. Rosenthal'],
     'E', None, ''),

    (226, ['Observational Cosmology', 'With the New Radio Surveys:',
           'Proceedings of a Workshop held in', 'Puerto de la Cruz, Tenerife, Canary',
           'Islands, Spain, 13-15 January 1997'], '1998', 
     ['M. N. Bremer', 'N. Jackson', 'I. Pérez-Fournon'],
     'E', None, ''),

    (227, ['Solar System Ices:', 'Based on Reviews Presented at the',
           'International Symposium “Solar', 'System Ices” held in Toulouse,',
           'France, on March 27--30, 1995'], '1998', 
     ['B. Schmitt', 'C. De Bergh', 'M. Festou'],
     'E', None, ''),

    (228, ['Optical Detectors for Astronomy:', 'Proceedings of an ESO CCD Workshop',
           'held in Garching, Germany,', 'October 8--10, 1996'], '1998', 
     ['James W. Beletic', 'Paola Amico'],
     'E', None, ''),

    (229, ['Observational Plasma Astrophysics:', 'Five Years of Yohkoh and Beyond'], '1998', 
     ['Tetsuya Watanabe', 'Takeo Kosugi', 'Alphonse C. Sterling'],
     'E', None, ''),

    (230, ['The Impact of Near-Infrared Sky', 'Surveys on Galactic and',
           'Extragalactic Astronomy:', 'Proceedings of the 3rd',
           'EUROCONFERENCE on Near-Infrared', 'Surveys held at Meudon Observatory,',
           'France, June 19-20, 1997'], '1998', 
     ['N. Epchtein'],
     'E', None, ''),

    (231, ['The Evolving Universe:', 'Selected Topics on Large-Scale',
           'Structure and on the Properties of', 'Galaxies'], '1998', 
     ['Donald Hamilton'],
     'E', None, ''),

    (233, ['B[e] Stars:', 'Proceedings of the Paris Workshop',
           'held from 9--12 June, 1997'], '1998', 
     ['Anne Marie Hubert', 'Carlos Jaschek'],
     'E', None, ''),

    (234, ['Observational Evidence for Black', 'Holes in the Universe:',
           'Proceedings of a Conference held in', 'Calcutta, India, January 10-17, 1998'], '1999', 
     ['Sandip K. Chakrabarti'],
     'E', None, ''),

    (235, ['Astrophysical Plasmas and Fluids'], '1999', 
     ['Vinod Krishan'],
     'A', None, ''),

    (236, ['Laboratory Astrophysics and Space', 'Research'], '1999', 
     ['P. Ehrenfreund', 'C. Krafft', 'H. Kochan', 'V. Pirronello'],
     'E', None, ''),

    (237, ['Post-Hipparcos Cosmic Candles'], '1999', 
     ['A. Heck', 'F. Caputo'],
     'E', None, ''),

    (238, ['Substorms-4'], '1999-03',
     ['S. Kokubun', 'Y. Kamide'],
     'E', '0-7923-5465-6', ''),

    (239, ['Motions in the Solar Atmosphere:', 'Proceedings of the Summer School and',
           'Workshop held at the Solar', 'Observatory Kanzelhöhe Kärnten,',
           'Austria, September 1-12, 1997'], '1999', 
     ['Arnold Hans', 'lmeier', 'Mauro Messerotti'],
     'E', None, ''),

    (240, ['Numerical Astrophysics:', 'Proceedings of the International',
           'Conference on Numerical Astrophysics', '1998 (NAP98), held at the National',
           'Olympic Memorial Youth Center,', 'Tokyo, Japan,March 10-13, 1998'], '1999', 
     ['Shoken M. Miyama', 'Kohji Tomisaka', 'Tomoyuki Hanawa'],
     'E', None, ''),

    (241, ['Millimeter-Wave Astronomy: Molecular', 'Chemistry \& Physics in Space:',
           'Proceedings of the 1996 INAOE Summer', 'School of Millimeter-wave Astronomy',
           'held at INAOE, Tonantzintla, Puebla,', 'Mexico, 15-31 July 1996'], '1999', 
     ['W. F. Wall', 'A. Carramiñana', 'L. Carrasco', 'P. F. Goldsmith'],
     'E', None, ''),

    (242, ['Cosmic Perspectives in Space Physics'], '2000', 
     ['Sukumar Biswas'],
     'A', None, ''),

    (243, ['Solar Polarization:', 'Proceedings of an International',
           'Workshop held in Bangalore, India,', '12-16 October, 1998'], '1999', 
     ['K. N. Nagendra', 'J. O. Stenflo'],
     'E', None, ''),

    (244, ['The Universe:', 'Visions and Perspectives'], '2000', 
     ['Naresh Dadhich', 'Ajit Kembhavi'],
     'E', None, ''),

    (245, ['Waves in Dusty Space Plasmas'], '2000', 
     ['Frank Verheest'],
     'A', None, ''),

    (246, ['The Legacy of J.C. Kapteyn:', 'Studies on Kapteyn and the',
           'Development of Modern Astronomy'], '2000', 
     ['P. C. Van Der Kruit', 'K. Van Berkel'],
     'A', None, ''),

    (247, ['Large Scale Structure Formation'], '2000', 
     ['Reza Mansouri', 'Robert Brandenberger'],
     'E', None, ''),

    (248, [], None,
     [],
     None, None, ''),

    (249, ['The Neutral Upper Atmosphere'], '2002', 
     ['S. N. Ghosh'],
     'A', None, ''),

    (250, ['Information Handling in Astronomy'], '2000', 
     ['André Heck'],
     'E', None, ''),

    (251, ['Cosmic Plasma Physics'], '2000', 
     ['Boris V. Somov'],
     'A', None, ''),

    (252, ['Optical Detectors For Astronomy II:', 'State of the Art at the Turn of the',
           'Millenium'], '2000', 
     ['Paola Amico', 'James W. Beletic'],
     'E', None, ''),

    (253, ['The Chemical Evolution of the Galaxy'], '2003', 
     ['Francesca Matteucci'],
     'A', None, ''),

    (254, ['Stellar Astrophysics:', 'Proceedings of the Pacific Rim',
           'Conference held in Hong Kong, 1999'], '2000', 
     ['K. S. Cheng', 'H. F. Chau', 'K. L. Chan', 'K. C. Leung'],
     'E', None, ''),

    (255, ['The Evolution of The Milky Way'], '2000', 
     ['Francesca Matteucci', 'Franco Giovannelli'],
     'E', None, ''),

    (256, ['Organizations and Strategies in', 'Astronomy'], '2000', 
     ['André Heck'],
     'E', None, ''),

    (257, ['Stellar Pulsation — Nonlinear', 'Studies'], '2001', 
     ['Mine Takeuti', 'Dimitar D. Sasselov'],
     'E', None, ''),

    (258, ['Electrohydrodynamics in Dusty and', 'Dirty Plasmas:',
           'Gravito-Electrodynamics and EHD'], '2001', 
     ['Hiroshi Kikuchi'],
     'A', None, ''),

    (259, ['The Dynamic Sun:', 'Proceedings of the Summer School and',
           'Workshop held at the Solar', 'Observatory, Kanzelhöhe, Känten,',
           'Austria, August 30 – September 10,', '1999'], '2001', 
     ['Arnold Hanslmeier', 'Mauro Messerotti', 'Astrid Veronig'],
     'E', None, ''),

    (260, ['Solar Cosmic Rays'], '2001', 
     ['Leonty I. Miroshnichenko'],
     'A', None, ''),

    (261, ['Collisional Processes in the Solar', 'System'], '2001', 
     ['Mikhail Ya. Marov', 'Hans Rickman'],
     'E', None, ''),

    (262, ['Whistler Phenomena:', 'Short Impulse Propagation'], '2001', 
     ['Csaba Ferencz', 'Orsolya E. Ferencz', 'Dániel Hamar', 'János Lichtenberger'],
     'E', None, ''),

    (263, ['New Horizons of Computational Science;',
           'Proceedings of the International',
           'Symposium on Supercomputing', 'held in Tokyo, Japan,',
           'September 1-3, 1997'], '2001', 
     ['T. Ebisuzaki', 'J. Makino'],
     'E', None, ''),

    (264, ['The Influence of Binaries on Stellar', 'Population Studies'], '2001', 
     ['Dany Vanbeveren'],
     'E', None, ''),

    (265, ['Post-AGB Objects as a Phase of', 'Stellar Evolution, Proceedsings of',
           'the Toruń Workshop held July 5-7,', '2000'], '2001', 
     ['Ryszard Szczerba', 'Sławomir K. Górny'],
     'E', None, ''),

    (266, ['Organizations and Strategies in', 'Astronomy, volume II'], '2001', 
     ['André Heck'],
     'E', None, ''),

    (267, ['The Nature of Unidentified Galactic', 'High-Energy Gamma-Ray Sources:',
           'Proceedings of the Workshop held at', 'Tonantzintla, Puebla, Mexico,',
           '9 -- 11 October 2000'], '2001', 
     ['Alberto Carramiñana', 'Olaf Reimer', 'David J. Thompson'],
     'E', None, ''),

    (268, ['Multielement System Design in', 'Astronomy and Radio Science'], '2001', 
     ['Lazarus E. Kopilovich', 'Leonid G. Sodin'],
     'A', None, ''),

    (269, ['Mechanics of Turbulence of', 'Multicomponent Gases'], '2001', 
     ['Mikhail Ya. Marov', 'Aleksander V. Kolesnichenko'],
     'A', None, ''),

    (270, ['Dayside and Polar Cap Aurora'], '2002', 
     ['Per Even Sandholt', 'Herbert C. Carlson', 'Alv Egeland'],
     'A', None, ''),

    (271, ['Astronomy-Inspired Atomic and', 'Molecular Physics'], '2002', 
     ['A. R. P. Rau'],
     'A', None, ''),

    (272, ['Merging Processes in Galaxy Clusters'], '2002', 
     ['L. Feretti', 'I. M. Gioia', 'G. Giovannini'],
     'E', None, ''),

    (273, ['Lunar Gravimetry:', 'Revealing the Far Side'], '2002', 
     ['Rune Floberghagen'],
     'A', None, ''),

    (274, ['New Quests in Stellar Astrophysics:', 'The Link Between Stars and', 'Cosmology:',
           'Proceedings of the International', 'Conference held in Puerto Vallarta,',
           'Mexico, 26-30 March 2001'], '2002', 
     ['Miguel Chávez', 'Alessandro Bressan', 'Alberto Buzzoni', 'Divakara Mayya'],
     'E', None, ''),

    (275, ['History of Oriental Astronomy:', 'Proceedings of the Joint',
           'Discussion-17 at the 23rd General', 'Assembly of the International',
           'Astronomical Union, organised by', 'Commission 41 (History of',
           'Astronomy), held in Kyoto, August', '25-26, 1997'], '2002', 
     ['S. M. Razaullah Ansari'],
     'E', None, ''),

    (276, ['Modern Theoretical and Observational', 'Cosmology:',
           'Proceedings of the 2nd Hellenic', 'Cosmology Meetings, held at the',
           'National Observatory of Athens,', 'Penteli, 19-20 April 2001'], '2002', 
     ['Manolis Plionis', 'Spiros Cotsakis'],
     'E', None, ''),

    (277, ['The Sun and Space Weather'], '2002', 
     ['Arnold Hanslmeier'],
     'A', None, ''),

    (278, ['Exploring the Secrets of the Aurora'], '2002', 
     ['Syun-Ichi Akasofu'],
     'A', None, ''),

    (279, ['Plasma Astrophysics:', 'Kinetic Processes in Solar and', 'Stellar Coronae'], '2002', 
     ['Arnold O. Benz'],
     'A', None, ''),

    (280, ['Organizations and Strategies in', 'Astronomy, volume III'], '2002', 
     ['André Heck'],
     'E', None, ''),

    (281, ['The IGM/Galaxy Connection:', 'The Distribution of Baryons at z=0'], '2003', 
     ['Jessica L. Rosenberg', 'Mary E. Putman'],
     'E', None, ''),

    (282, ['Radio Recombination Lines:', 'Their Physics and Astronomical', 'Applications'], '2009', 
     ['M.A. Gordon', 'R.L. Sorochenko'],
     'A', None, ''),

    (283, ['Mass-Losing Pulsating Stars and', 'their Circumstellar Matter:',
           'Observations and Theory'], '2003', 
     ['Y. Nakada', 'M. Honma', 'M. Seki'],
     'E', None, ''),

    (284, ['Light Pollution: The Global View:', 'Proceedings of the International',
           'Conference on Light Pollution, La', 'Serena, Chile, held 5-7 March 2002'], '2003', 
     ['Hugo E. Schwarz'],
     'E', None, ''),

    (285, ['Information Handling in Astronomy ---', 'Historical Vistas'], '2002', 
     ['André Heck'],
     'E', None, ''),

    (286, ['Searching the Heavens and the Earth:', 'The History of Jesuit Observatories'], '2003', 
     ['Augustín Udías'],
     'A', None, ''),

    (287, ['The Future of Small Telescopes in', 'the New Millennium'], '2003', 
     ['Terry D. Oswalt'],
     'E', None, ''),

    (288, ['The Future of Small Telescopes in', 'the New Millennium'], '2003', 
     ['Terry D. Oswalt'],
     'E', None, ''),

    (289, ['The Future of Small Telescopes in', 'the New Millennium'], '2003', 
     ['Terry D. Oswalt'],
     'E', None, ''),

    (290, ['Astronomy Communication'], '2003', 
     ['André Heck', 'Claus Madsen'],
     'E', None, ''),

    (291, ['Dynamical Systems and Cosmology'], '2003', 
     ['A. A. Coley'],
     'A', None, ''),

    (292, ['Whatever Shines Should be Observed:', 'Quicquid Nitet Notandum),'], '2003', 
     ['Susan M. P. McKenna-Lawlor'],
     'A', None, ''),

    (293, ['Physics of the Solar System:', 'Dynamics and Evolution, Space',
           'Physics, and Spacetime Structure'], '2003', 
     ['Bruno Bertotti', 'Paolo Farinella', 'David Vokrouhlický'],
     'A', None, ''),

    (294, ['An Introduction to Plasma', 'Astrophysics and', 'Magnetohydrodynamics'], '2003', 
     ['Marcel Goossens'],
     'A', None, ''),

    (295, ['Integrable Problems of Celestial', 'Mechanics in Spaces of Constant',
           'Curvature'], '2003', 
     ['Tatiana G. Vozmischeva'],
     'A', None, ''),

    (296, ['Organizations and Strategies in', 'Astronomy, volume IV'], '2003', 
     ['André Heck'],
     'E', None, ''),

    (297, ['Radiation Hazard in Space'], '2003', 
     ['Leonty I. Miroshnichenko'],
     'A', None, ''),

    (298, ['Stellar Astrophysics — A Tribute to', 'Helmut A. Abt'], '2003', 
     ['K. S. Cheng', 'K. C. Leung', 'T. P. Li'],
     'E', None, ''),

    (299, ['Open Issues in Local Star Formation'], '2003', 
     ['Jacques Lépine', 'Jane Gregorio-Hetem'],
     'E', None, ''),

    (300, ['Scientific Detectors for Astronomy:', 'The Beginning of a New Era'], '2004', 
     ['Paola Amico', 'James W. Beletic', 'Jenna E. Beletic'],
     'E', None, ''),

    (301, ['Multiwavelength Cosmology:', 'Proceedings of the “Multiwavelength',
           'Cosmology” Conference, held on', 'Mykonos Island, Greece,', '17–20 June, 2003'], '2004', 
     ['Manolis Plionis'],
     'E', None, ''),

    (302, ['Stellar Collapse'], '2004', 
     ['Chris L. Fryer'],
     'E', None, ''),

    (303, ['Cosmic Rays in the Earth’s', 'Atmosphere and Underground'], '2004', 
     ['Lev I. Dorman'],
     'A', None, ''),

    (304, ['Cosmic Gamma-Ray Sources'], '2004', 
     ['K. S. Cheng', 'Gustavo E. Romero'],
     'E', None, ''),

    (305, ['Astrobiology: Future Perspectives'], '2005', 
     ['Pascale Ehrenfreund', 'William Irvine', 'Toby Owen', 'Luann Becker', 'Jen Blank', 'John Brucato', 'Luigi Colangeli', 'Sylvie Derenne', 'Anne Dutrey', 'Didier Despois', 'Antonio Lazcano', 'Francois Robert'],
     'E', None, ''),

    (306, ['Polytropes:', 'Applications in Astrophysics and', 'Related Fields'], '2004', 
     ['G. P. Horedt'],
     'A', None, ''),

    (307, ['Polarization in Spectral Lines'], '2004', 
     ['Egidio Landi Degl’innocenti', 'Marco Landolfi'],
     'A', None, ''),

    (308, ['Supermassive Black Holes in the', 'Distant Universe'], '2004', 
     ['Amy J. Barger'],
     'E', None, ''),

    (309, ['Soft X-Ray Emission from Clusters of', 'Galaxies and Related Phenomena'], '2004', 
     ['Richard Lieu', 'Jonathan Mittaz'],
     'E', None, ''),

    (310, ['Organizations and Strategies in', 'Astronomy, volume V'], '2004', 
     ['André Heck'],
     'E', None, ''),

    (311, ['The New Rosetta Targets:', 'Observations, Simulations and',
           'Instrument Performance'], '2004', 
     ['Luigi Colangeli', 'Elena Mazzotta Epifani', 'Pasquale Palumbo'],
     'E', None, ''),

    (312, ['High-Velocity Clouds'], '2005', 
     ['Hugo van Woerden', 'Bart P. Wakker', 'Ulrich J. Schwarz', 'Klaas S. de Boer'],
     'E', None, ''),

    (313, ['Adventures in Order and Chaos:', 'A Scientific Autobiography'], '2004', 
     ['George Contopoulos'],
     'A', None, ''),

    (314, ['Solar and Space Weather', 'Radiophysics:', 'Current Status and Future',
           'Developments'], '2005', 
     ['Dale E. Gary', 'Christoph U. Keller'],
     'E', None, ''),

    (315, ['How does the Galaxy Work?:',
           'A Galactic Tertulia with Don Cox and', 'Ron Reynolds'], '2005', 
     ['Emilio J. Alfaro', 'Enrique Pérez', 'José Franco'],
     'E', None, ''),

    (316, ['Civic Astronomy:', 'Albany’s Dudley Observatory,', '1852--2002'], '2004', 
     ['George Wise'],
     'A', None, ''),

    (317, ['The Sun and the Heliosphere as an', 'Integrated System'], '2004', 
     ['Giannina Poletto', 'Steven T. Suess'],
     'E', None, ''),

    (318, ['Transfer of Polarized Light in', 'Planetary Atmospheres:',
           'Basic Concepts and Practical Methods'], '2004', 
     ['Joop W. Hovenier', 'Cornelis Van Der Mee', 'Helmut Domke'],
     'A', None, ''),

    (319, ['Penetrating Bars through Masks of', 'Cosmic Dust:',
           'The Hubble Tuning Fork strikes a New', 'Note'], '2004', 
     ['David L. Block', 'Ivânio Puerari', 'Kenneth C. Freeman', 'Robert Groess', 'Elizabeth K. Block'],
     'E', None, ''),

    (320, ['Solar Magnetic Phenomena:', 'Proceedings of the 3rd Summer School',
           'and Workshop held at the Solar', 'Observatory Kanzelhöhe, Känten,', 'Austria, August 25 --- September 5.', '2003'], '2005', 
     ['Arnold Hanslmeier', 'Astrid Veronig', 'Mauro Messerotti'],
     'E', None, ''),

    (321, ['Nonequilibrium Phenomena in Plasmas'], '2005', 
     ['W.B. Burton', 'J. M. E. Kuijpers', 'E. P. J. Van Den Heuvel', 'H. Van Der Laan', 'I. Appenzeller', 'J. N. Bahcall', 'F. Bertola', 'J. P. Cassinelli', 'C. J. Cesarsky', 'O. Engvold', 'R. McCray', 'P. G. Murdin', 'F. Pacini', 'V. Radhakrishnan', 'K. Sato', 'F. H. Shu', 'B. V. Somov', 'R. A. Sunyaev', 'Y. Tanaka', 'S. Tremaine', 'N. O. Weiss', 'A. Surjalal Sharma', 'Predhiman K. Kaw'],
     'E', None, ''),

    (322, ['Light Pollution Handbook'], '2004', 
     ['Kohei Narisada', 'Duco Schreuder'],
     'E', None, ''),

    (323, ['Recollections of “Tucson', 'Operations”:', 'The Millimeter-Wave Observatory of',
           'the National Radio Astronomy', 'Observatory'], '2005', 
     ['M. A. Gordon'],
     'A', None, ''),

    (324, ['Cores to Clusters:', 'A Scientific Autobiography'], '2005', 
     ['M. S. N. Kumar', 'M. Tafalla', 'P. Caselli'],
     'E', None, ''),

    (325, ['Kristian Birkeland:', 'The First Space Scientist'], '2005', 
     ['Alv Egeland', 'William J. Burke'],
     'A', None, ''),

    (326, ['Neutron Stars 1'], '2007', 
     ['P. Haensel', 'A. Y. Potekhin', 'D. G. Yakovlev'],
     'E', None, ''),

    (327, ['The Initial Mass Function 50 Years', 'Later'], '2005', 
     ['Edvige Corbelli', 'Francesco Palla', 'Hans Zinnecker'],
     'E', None, ''),

    (328, ['Comets:', 'Nature, Dynamics, Origin, and the', 'Cosmological Relevance'], '2005', 
     ['Julio Angel Fernández'],
     'A', None, ''),

    (329, ['Starbursts:', 'From 30 Doradus to Lyman Break', 'Galaxies'], '2005', 
     ['Richard De Grijs', 'Rosa M. González Delgado'],
     'E', None, ''),

    (330, ['The Multinational History of', 'Strasbourg Astronomical Observatory'], '2005', 
     ['André Heck'],
     'E', None, ''),

    (331, ['Ultraviolet Radiation in the Solar', 'System'], '2006', 
     ['M. Vázquez', 'A. Hanslmeier'],
     'A', None, ''),

    (332, ['White Dwarfs: Cosmological and', 'Galactic Probes'], '2005', 
     ['Edward M. Sion', 'Stéphane Vennes', 'Harry L. Shipman'],
     'E', None, ''),

    (333, ['Planet Mercury'], '2005-11',
     ['P. Clark', 'S. McKenna-Lawlor'],
     'A', '1-387-26358-6', ''),

    (334, ['The New Astronomy: Opening the', 'Electromagnetic Window and Expanding',
           'Our View of Planet Earth:', 'A Meetings to Honor Woody Sullivan',
           'on his 60th Birthday'], '2005', 
     ['Wayne Orchiston'],
     'E', None, ''),

    (335, ['Organizations and Strategies in', 'Astronomy Volume 6'], '2006', 
     ['André Heck'],
     'E', None, ''),

    (336, [], None, 
     [],
     None, None, ''),

    (337, [], None, 
     [],
     None, None, ''),

    (338, ['Solar Journey:', 'The Significance of our Galactic',
           'Environment for the Heliosphere and', 'Earth'], '2006', 
     ['Priscilla C.Frisch'],
     'E', None, ''),

    (339, ['Cosmic Ray Interactions,', 'Propagation, and Acceleration in',
           'Space Plasmas'], '2006', 
     ['Lev I. Dorman'],
     'A', None, ''),

    (340, ['Plasma Astrophysics:', 'Part I,  Fundamentals and Practice'], '2006', 
     ['Boris V. Somov'],
     'A', None, ''),

    (341, ['Plasma Astrophysics'], '2007', 
     ['Boris V. Somov'],
     'A', None, ''),

    (342, ['The Astrophysics of Emission-Line', 'Stars'], '2007', 
     ['Tomokazu Kogure', 'Kam-Ching Leung'],
     'A', None, ''),

    (343, ['Organizations and Strategies in', 'Astronomy volume 7'], '2006', 
     ['André Heck'],
     'E', None, ''),

    (344, ['Space Weather:', 'Research Towards Applications in', 'Europe'], '2007', 
     ['Jean Lilensten'],
     'E', None, ''),

    (345, ['Canonical Perturbation Theories:', 'Degenerate Systems and Resonance'], '2007', 
     ['Sylvio Ferraz-Mello'],
     'A', None, ''),

    (346, [], None, 
     [],
     None, None, ''),

    (347, ['The Sun and Space Weather, 2nd', 'edition'], '2007', 
     ['Arnold Hanslmeier'],
     'A', None, ''),

    (348, ['The Paraboloidal Reflector Antenna', 'in Radio Astronomy and', 'Communication:',
           'Theory and Practice'], '2007', 
     ['Jacob W. M. Baars'],
     'A', None, ''),

    (349, ['Lasers, Clocks and Drag-Free', 'Control:', 'Exploration of Relativistic Gravity',
           'in Space'], '2008', 
     ['Hansjorg Dittus', 'Claus Lammerzahl', 'Slava G. Turyshev'],
     'E', None, ''),

    (350, ['Hipparcos, the New Reduction of the', 'Raw Data'], '2007', 
     ['Floor van Leeuwen'],
     'E', None, ''),

    (351, ['High Time Resolution Astrophysics'], '2008', 
     ['Don Phelan', 'Oliver Ryan', 'Andrew Shearer'],
     'E', None, ''),

    (352, ['Short-Period Binary Stars:', 'Observations, Analyses, and Results'], '2008', 
     ['Eugene F. Milone', 'Denis A. Leahy', 'David W. Hobill'],
     'A', None, ''),

    (353, ['Hydromagnetic Waves in the', 'Magnetosphere and the Ionosphere'], '2007', 
     ['Professor Leonid S. Alperovich', 'Professor Evgeny N. Fedorov'],
     'A', None, ''),

    (354, ['Sirius Matters'], '2008', 
     ['Noah Brosch'],
     'A', None, ''),

    (355, ['Black Hole Gravitohydromagnetics'], '2009', 
     ['Brian Punsly'],
     'A', None, ''),

    (356, ['The Science of Solar System Ices'], '2013', 
     ['Murthy S. Gudipati', 'Julie Castillo-Rogez'],
     'E', None, ''),

    (357, ['Neutron Stars and Pulsars'], '2009', 
     ['Werner Becker'],
     'E', None, ''),

    (358, ['Cosmic Rays in Magnetospheres of the', 'Earth and other Planets'], '2009', 
     ['Lev Dorman'],
     'A', None, ''),

    (359, ['Physics of Relativistic Objects in', 'Compact Binaries: From Birth to',
           'Coalescence'], '2009', 
     ['Monica Colpi', 'Piergiorgio Casella', 'Vittorio Gorini', 'Ugo Moschella',
      'Andrea Possenti'],
     'E', None, ''),

    (360, ['The Principles of Astronomical', 'Telescope Design'], '2009', 
     ['Jingquan Cheng'],
     'A', None, ''),

    (361, ['The Sun Recorded Through History:', 'Scientific Data Extracted from',
           'Historical Documents'], '2009', 
     ['M. Vázquez', 'M. Vaquero'],
     'A', None, ''),

    (362, ['Nonlinear Cosmic Ray Diffusion', 'Theories'], '2009', 
     ['Andreas Shalchi'],
     'A', None, ''),

    (363, ['Under the Radar:', 'The First Woman in Radio Astronomy:', 'Ruby Payne-Scott'], '2010', 
     ['Prof. W. M. Goss', 'Dr. Richard X. McGee'],
     'E', None, ''),

    (364, ['Thermal Design and Thermal Behaviour', 'of Radio Telescopes and their',
           'Enclosures'], '2010', 
     ['Albert Greve', 'Michael Bremer'],
     'A', None, ''),

    (365, ['Solar Neutrons and Related Phenomena'], '2010', 
     ['Lev Dorman'],
     'A', None, ''),

    (366, ['Planets in Binary Star Systems'], '2010', 
     ['Nader Haghighipour'],
     'E', None, ''),

    (367, ['General Relativity and John', 'Archibald Wheeler'], '2010', 
     ['Ignazio Ciufolini', 'Richard A. Matzner'],
     'E', None, ''),

    (368, ['Water in the Universe'], '2011', 
     ['Arnold Hanslmeier'],
     'A', None, ''),

    (369, ['Jacobi Dynamics:', 'A Unified Theory with Applications',
           'to Geophysics, Celestial Mechanics,', 'Astrophysics and Cosmology'], '2011', 
     ['V.I. Ferronsky', 'S.A. Denisik', 'S.V. Ferronsky'],
     'A', None, ''),

    (370, ['Dark Matter and Dark Energy:', 'A Challenge to Modern Cosmology'], '2011', 
     ['Sabino Matarrese', 'Monica Colpi', 'Vittorio Gorini', 'Ugo Moschella'],
     'E', None, ''),

    (371, ['Linear Isentropic Oscillations of', 'Stars:', 'Theoretical Foundations'], '2010', 
     ['Paul Smeyers', 'Tim Van Hoolst'],
     'A', None, ''),

    (372, ['Kinetic Theory of the Inner', 'Magnetospheric Plasma'], '2011', 
     ['George V. Khazanov'],
     'A', None, ''),

    (373, ['Astronomical Photometry:', 'Past, Present, and Future'], '2011', 
     ['Eugene F. Milone', 'C. Sterken'],
     'E', None, ''),

    (374, ['Heaven and Earth in Ancient Greek', 'Cosmology:',
           'From Thales to Heraclides Ponticus'], '2011', 
     ['Dirk L. Couprie'],
     'A', None, ''),

    (375, ['Fine Structure of Solar Radio Bursts'], '2011', 
     ['Gennady P. Chernov'],
     'A', None, ''),

    (376, ['Coronal Mass Ejections:', 'An Introduction'], '2011', 
     ['Timothy Howard'],
     'A', None, ''),

    (377, ['Integrated Modeling of Telescopes'], '2011', 
     ['Torben Andersen', 'Anita Enmark'],
     'A', None, ''),

    (378, ['Hot Interstellar Matter in', 'Elliptical Galaxies'], '2012', 
     ['Dong-Woo Kim', 'Silvia Pellegrini'],
     'E', None, ''),

    (379, ['The Spiral Galaxy M33'], '2012', 
     ['P. Hodge'],
     'A', None, ''),

    (380, ['The Astronomer Jules Janssen:', 'A Globetrotter of Celestial Physics'], '2012', 
     ['Françoise Launay'],
     'A', None, ''),

    (381, ['Taking the Back off the Watch:', 'A Personal Memoir'], '2012', 
     ['Thomas Gold aut.', 'Simon Mitton'],
     'E', None, ''),

    (382, ['A Brief History of Radio Astronomy', 'in the USSR:',
           'A Collection of Scientific Essays'], '2012', 
     ['S. Y. Braude', 'A. E. Salomonovich', 'V. A. Samanian', 'I. S. Shklovskii', 'R. L. Sorochenko', 'V. S. Troitskii', 'K. I. Kellermann', 'B. A. Dubinskii', 'N. L. Kaidanovskii', 'N. S. Kardashev', 'M. M. Kobrin', 'A. D. Kuzmin', 'A. P. Molchanov', 'Yu. N. Pariiskii', 'O. N. Rzhiga'],
     'E', None, ''),

    (383, ['Fundamental Questions of Practical', 'Cosmology:',
           'Exploring the Realm of Galaxies'], '2012', 
     ['Yurij Baryshev', 'Pekka Teerikorpi'],
     'A', None, ''),

    (384, ['Eta Carinae and the Supernova', 'Impostors'], '2012', 
     ['Kris Davidson', 'Roberta M. Humphreys'],
     'E', None, ''),

    (385, ['Nanodust in the Solar System:', 'Discoveries and Interpretations'], '2012', 
     ['Ingrid Mann', 'Nicole Meyer-Vernet', 'Andrzej Czechowski'],
     'E', None, ''),

    (386, ['Fifty Years of Quasars:', 'From Early Observations and Ideas to',
           'Future Research'], '2012', 
     ["Mauro D'Onofrio", 'Paola Marziani', 'Jack W. Sulentic'],
     'E', None, ''),

    (387, ['The Synthesis of the Elements:', 'The Astrophysical Quest for',
           'Nucleosynthesis and What It Can Tell', 'Us About the Universe'], '2012', 
     ['Giora Shaviv'],
     'A', None, ''),

    (388, ['Cosmic Electrodynamics:', 'Electrodynamics and Magnito',
           'Hydrodynamics of Cosmic Plasma'], '2013', 
     ['Gregory D. Fleishman', 'Igor N. Toptygin'],
     'A', None, ''),

    (389, ['Turbulence and Self-Organization:', 'Modeling Astrophysical Objects'], '2013', 
     ['Mikhail Ya Marov', 'Aleksander V. Kolesnichenko'],
     'A', None, ''),

    (390, ['In Search of William Gascoigne:', 'Seventeenth Century Astronomer'], '2012', 
     ['David Sellers'],
     'A', None, ''),

    (391, ['Plasma Astrophysics, Part I:', 'Fundamentals and Practice'], '2012', 
     ['Boris V. Somov'],
     'A', None, ''),

    (392, ['Plasma Astrophysics, Part II:', 'Reconnection and Flares'], '2013', 
     ['Boris V. Somov'],
     'A', None, ''),

    (393, ['Carl Størmer:', 'Auroral Pioneer'], '2013', 
     ['Alv Egeland', 'William J. Burke'],
     'A', None, ''),

    (394, ['How Einstein Created Relativity out', 'of Physics and Astronomy'], '2013', 
     ['David Topper'],
     'A', None, ''),

    (395, ['Georges Lemaître: Life, Science and', 'Legacy'], '2012', 
     ['Rodney D. Holder', 'Simon Mitton'],
     'E', None, ''),

    (396, ['The First Galaxies:', 'Theoretical Predictions and', 'Observational Clues'], '2013', 
     ['Tommy Wiklind', 'Bahram Mobasher', 'Volker Bromm'],
     'E', None, ''),

    (397, ['Le Verrier—Magnificent and', 'Detestable Astronomer'], '2013', 
     ['James Lequeux'],
     'A', None, ''),

    (398, ['The Great Refractor of Meudon', 'Observatory'], '2013', 
     ['Audouin Dollfus'],
     'A', None, ''),

    (399, ['The Stars of Galileo Galilei and the', 'Universal Knowledge of Athanasius',
           'Kircher'], '2014', 
     ['Roberto Buonanno'],
     'A', None, ''),

    (400, ['The Coronas-F Space Mission:', 'Key Results for Solar Terrestrial', 'Physics'], '2014', 
     ['Vladimir Kuznetsov'],
     'E', None, ''),

    (401, ['50 Years of Brown Dwarfs:', 'From Predictions to Discovery to',
           'Forefront of Research'], '2014', 
     ['Viki Joergens'],
     'E', None, ''),

    (402, ['Opacity'], '2014', 
     ['Walter F. Huebner', 'W. David Barfield'],
     'A', None, ''),

    (403, ['Dynamics of Magnetically Trapped', 'Particles:', 'Foundations of the Physics of',
           'Radiation Belts and Space Plasmas'], '2014', 
     ['Juan G. Roederer', 'Hui Zhang'],
     'A', None, ''),

    (404, ['Advanced Interferometers and the', 'Search for Gravitational Waves:',
           'Lectures from the First VESF School', 'on Advanced Detectors for',
           'Gravitational Waves'], '2014', 
     ['Massimo Bassan'],
     'E', None, ''),

    (405, ['Solar Cosmic Rays:', 'Fundamentals and Applications'], '2015', 
     ['Leonty Miroshnichenko'],
     'A', None, ''),

    (406, ['Eclipses, Transits, and Comets of', 'the Nineteenth Century:',
           'How America’s Perception of the', 'Skies Changed'], '2015', 
     ['Stella Cottam', 'Wayne Orchiston'],
     'A', None, ''),

    (407, ['Magnetic Fields in Diffuse Media'], '2015', 
     ['Alexander Lazarian', 'Elisabete M. de Gouveia Dal Pino', 'Claudio Melioli'],
     'E', None, ''),

    (408, ['Giants of Eclipse: The $\zeta$ Aurigae', 'Stars and Other Binary Systems'], '2015', 
     ['Thomas B. Ake', 'Elizabeth Griffin'],
     'E', None, ''),

    (409, ["Camille Flammarion's The Planet", 'Mars:', 'as translated by Patrick Moore'], '2015', 
     ['William Sheehan'],
     'E', None, ''),

    (410, ['Celestial Shadows:', 'Eclipses, Transits, and Occultations'], '2015', 
     ['John Westfall', 'William Sheehan'],
     'A', None, ''),

    (411, ['Characterizing Stellar and', 'Exoplanetary Environments'], '2015', 
     ['Helmut Lammer', 'Maxim Khodachenko'],
     'E', None, ''),

    (412, ['Very Massive Stars in the Local', 'Universe'], '2015', 
     ['Jorick S. Vink'],
     'E', None, ''),

    (413, ['Ecology of Blue Straggler Stars'], '2015', 
     ['Henri M. J. Boffin', 'Giovanni Carraro', 'Giacomo Beccari'],
     'E', None, ''),

    (414, ['The Formation and Disruption of', 'Black Hole Jets'], '2015', 
     ['Ioannis Contopoulos', 'Denise Gabuzda', 'Nikolaos Kylafis'],
     'E', None, ''),

    (415, ['Solar Prominences'], '2015', 
     ['Jean-Claude Vial', 'Oddbjørn Engvold'],
     'E', None, ''),

    (416, ['Jacobus Cornelius Kapteyn:', 'Born Investigator of the Heavens'], '2015', 
     ['Pieter C. van der Kruit'],
     'A', None, ''),

    (417, ['Physics of Magnetic Flux Tubes'], '2015', 
     ['Margarita Ryutova'],
     'A', None, ''),

    (418, ['Galactic Bulges'], '2016', 
     ['Eija Laurikainen', 'Reynier Peletier', 'Dimitri Gadotti'],
     'E', None, ''),

    (419, ['The Starlight Night:', 'The Sky in the Writings of',
           'Shakespeare, Tennyson, and Hopkins'], '2016', 
     ['David H. Levy'],
     'A', None, ''),

    (420, ['Tidal Streams in the Local Group and', 'Beyond:',
           'Observations and Implications'], '2016', 
     ['Heidi Jo Newberg', 'Jeffrey L. Carlin'],
     'E', None, ''),

    (421, ['François Arago:', 'A 19th Century French Humanist and',
           'Pioneer in Astronomy'], '2016', 
     ['James Lequeux'],
     'A', None, ''),

    (422, ['Exploring the History of New Zealand', 'Astronomy:',
           'Trials, Tribulations, Telescopes and', 'Transits'], '2016', 
     ['Wayne Orchiston'],
     'A', None, ''),

    (423, ['Understanding the Epoch of Cosmic', 'Reionization:',
           'Challenges and Progress'], '2016', 
     ['Andrei Mesinger'],
     'E', None, ''),

    (424, ['The Birth of Star Clusters'], '2018', 
     ['Dr. Steven Stahler'],
     'E', None, ''),

    (425, ['Lunar and Planetary Cartography in', 'Russia'], '2016', 
     ['Vladislav Shevchenko', 'Zhanna Rodionova', 'Gregory Michael'],
     'A', None, ''),

    (426, ['Low Frequency Radio Astronomy',
           'and the LOFAR Observatory'], '2019', 
     ['George Heald', 'John McKean', 'Roberto Pizzo'],
     'E', '978-3-319-23433-5', ''),

    (427, ['Magnetic Reconnection:', 'Concepts and Applications'], '2016', 
     ['Walter Gonzalez', 'Eugene Parker'],
     'E', None, ''),

    (428, ['Methods of Detecting Exoplanets:', '1st Advanced School on Exoplanetary',
           'Science'], '2016', 
     ['Valerio Bozza', 'Luigi Mancini', 'Alessandro Sozzetti'],
     'E', None, ''),

    (429, [], None, 
     [],
     None, None, ''),

    (430, ['Gas Accretion onto Galaxies'], '2017', 
     ['Andrew Fox', 'Romeel Davé'],
     'E', None, ''),

    (431, [], None, 
     [],
     None, None, ''),

    (432, [], None, 
     [],
     None, None, ''),

    (433, [], None, 
     [],
     None, None, ''),

    (434, ['Outskirts of Galaxies'], '2017', 
     ['Johan H. Knapen', 'Janice C. Lee', 'Armando Gil de Paz'],
     'E', None, ''),

    (435, ['From the Realm of the Nebulae to', 'Populations of Galaxies:',
           'Dialogues on a Century of Research'], '2016', 
     ["Mauro D'Onofrio", 'Roberto Rampazzo', 'Simone Zaggia'],
     'E', None, ''),

    (436, ['Celestial Mechanics and', 'Astrodynamics: Theory and Practice'], '2016', 
     ['Pini Gurfil', 'P. Kenneth Seidelmann'],
     'A', None, ''),

    (437, ['Oscillations of Disks'], '2016', 
     ['Shoji Kato'],
     'A', None, ''),

    (438, ['Energetic Particles in the', 'Heliosphere'], '2017', 
     ['George M. Simnett'],
     'A', None, ''),

    (439, ['Astronomy at High Angular', 'Resolution:', 'A Compendium of Techniques in the',
           'Visible and Near-Infrared'], '2016', 
     ['Henri M. J. Boffin', 'Gaitee Hussain', 'Jean-Philippe Berger', 'Linda Schmidtobreick'],
     'E', None, ''),

    (440, ['Astrophysics of Black Holes:', 'From Fundamental Aspects to Latest',
           'Developments'], '2016', 
     ['Cosimo Bambi'],
     'E', None, ''),

    (441, ['The Lidov-Kozai Effect ---', 'Applications in Exoplanet Research',
           'and Dynamical Astronomy'], '2017', 
     ['Ivan I. Shevchenko'],
     'A', None, ''),

    (442, ['A Dirty Window:', 'Diffuse and Translucent Molecular',
           'Gas in the Interstellar Medium'], '2017', 
     ['Loris Magnani', 'Steven N. Shore'],
     'A', None, ''),

    (443, ['The Three-Body Problem and the', 'Equations of Dynamics:',
           'Poincaré’s Foundational Work on', 'Dynamical Systems'], '2017', 
     ['Henri Poincaré'],
     'A', None, ''),

    (444, ['Solar Particle Radiation Storms', 'Forecasting and Analysis:',
           'The HESPERIA HORIZON 2020 Project and', 'Beyond'], '2018', 
     ['Dr. Olga E. Malandraki', 'Dr. Norma B. Crosby'],
     'E', None, ''),

    (445, ['Formation, Evolution, and Dynamics', 'of Young Solar Systems'], '2017', 
     ['Prof. Martin Pessah', 'Prof. Oliver Gressel'],
     'E', None, ''),

    (446, ['Modelling Pulsar Wind Nebulae'], '2017', 
     ['Prof. Diego F. Torres'],
     'E', None, ''),

    (447, ['Radio Telescope Reflectors:', 'Historical Development of Design and',
           'Construction'], '2018', 
     ['Dr. Jacob W. M. Baars', 'Dr. Hans J Kärcher'],
     'A', None, ''),

    (448, ['Magnetic Fields in the Solar System:', 'Planets, Moons and Solar Wind',
           'Interaction'], '2018', 
     ['Hermann Lühr', 'Johannes Wicht', 'Stuart A. Gilder', 'Matthias Holschneider'],
     'E', None, ''),

    (449, ['First Ten Years of Hinode Solar', 'On-Orbit Observatory'], '2018', 
     ['Prof. Toshifumi Shimizu', 'Prof. Shinsuke Imada', 'Dr. Masahito Kubo'],
     'E', '978-981-10-7741-8', ''),

    (450, ['Astrophysics of Exoplanetary', 'Atmospheres:',
           '2nd Advanced School on Exoplanetary', 'Science'], '2018', 
     ['Prof. Dr. Valerio Bozza', 'Dr. Luigi Mancini', 'Prof. Dr. Alessandro Sozzetti'],
     'E', '978-3-319-89700-4', ''),

    (451, ['Laboratory Astrophyscs'], '2018',
     ['Caro Mu\~{n}oz', 'M. Guillermo', 'Rafael Escribano'],
     'E', '978-3-319-90019-3', ''),

    (452, [], None,
     [],
     None, None, ''),

    (453, ['Astrophysics with Radioactive Isotopes'], '2018',
     ['Roland Diehl', 'Dieter Hartmann', 'Nikos Prantzos'],
     'E', '978-3-319-91928-7', ''),

    (454, ['Accretion Flows in Astrophysics'], '2018',
     ['Nikolay Shakura'],
     'E', '978-3-319-93008-4', ''),

    (455, ['Physics of Magnetic Flux Tubes'], '2018',
     ['Margarita Ryutova'],
     'A', '978-3-319-96360-0', ''),

    (456, ['Magnetohydodynamics in Binary Stars'], '2018',
     ['C. G. Campell'],
     'A', '978-3-319-97654-7', ''),

    (457, ['The Physics and Astrophysics of Neutron Stars'], '2018',
     ['L. Rezzolla', 'P. Pizzochero', 'D.~I. Jones', 'N. Rea', 'I. Vidana'],
     'E', '978-3-319-97615-0', ''),

    (458, ['New Millennium Solar Physics'], '2019',
     ['Markus J. Aschwanden'],
     'A', '978-3-030-13954-4', ''),

    (459, ['Jan Hendrik Oort:', 'Master of the Galactic System'], '2019',
     ['Pieter C. van der Kruit'],
     'A', '978-3-030-17800-0', ''),

    (460, ['Astronomical Polarization from', 'Infrared to Gamma Rays'], '2019',
     ['R. Mignani', 'A. Shearer', 'A. Slowikowska', 'S. Zane'],
     'E', '978-3-030-19714-8', ''),

    (461, ['Timing Neutron Stars:', 'Pulsations, Oscillations and Explosions'], '2021',
     ['Tomaso Belloni', 'Mariano Méndez', 'Chengmin Zhang'],
     'E', '978-3-662-62108-0', ''),

    (462, ['High Energy Cosmic Rays'], '2021',
     ['Todor Stanev'],
     'A', '978-3-030-71566-3', ''),

    (463, ['Dynamical Chaos in Planetary Systems'], '2020',
     ['Ivan Schevchenko'],
     'A', '978-3-030-52143-1', ''),

    (464, ['Kappa Distributions:', 'From Observational Evidences via Controversial',
           'Predictions to a Consistent Theory of', 'Nonequilibrium Plasmas'], '2021',
     ['Marian Lazar', 'Horst Fichtner'],
     'E', '978-3-030-82622-2', '')
    
]

def assl_print_books(book_list):
    '''Print the book list in assl_table in long table format.'''

    for count, entry in enumerate(book_list):
        try:
            volnum = entry[0]
            title_list = entry[1]
            year = entry[2]
            author_list = entry[3]
            ae_flag = entry[4]
            isbn = entry[5]
            ajbnum = entry[6]
        except:
            print('failed to read entry', count, file=sys.stderr)
            continue
        
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
    tb.print_table_heading(4, TBL_HEADING, CONTINUE_LABEL)
    tb.print_table_footer(TBL_FOOTER, CONTINUE_FOOTER)

    assl_print_books(ASSL_BOOK_LIST)
    tb.print_table_end()

