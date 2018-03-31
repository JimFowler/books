#
# The listings to create the table
#  asslKluwer_table.tex
#
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
    #( volnum, title_list, copyright, [authors/editors list] )
    (216, ['Magnetohydrodynamics in',
           'Binary Stars'], 1997,
     ['C. G. Campbell']),

    (217, ['Nonequilibrium Processes',
           'in the Planetary and Cometary',
           'Atmospheres'], 1997,
     ['Valery I. Shematovich', 'Dmitry V. Bisikalo', 'Jean-Claude Gérard']),

    (218, ['Astronomical Time Series'], 1997,
     ['Dan Maoz', 'Amiel Sternberg', 'Elia M. Leibowitz']),

    (219, ['The Interstellar Medium in Galaxies'], 1997,
     ['J. M. van der Hulst']),

    (220, ['The Three Galileos:',
           'The Man, The Spacecraft,',
           'The Telescope'], 1997,
     ['Cesare Barbiere', 'Jürgen H. Rahe', 'Torrence V. Johnson', 'Anita M. Sohus']),

    (221, [], None, []),

    (222, ['Remembering Edith Alice Müller'], 1998,
     ['Yves Chmielewski','Jean-Claude Pecker', 'Ramiro de la Reza', 'Gustav Tammann',
      'Patrick A. Wayman']),

    (223, ['Visual Double Stars: Formation,',
           'Dynamics and Evolutionary Tracks'], 1997,
     ['A. Elipe', 'H. McAlister']),

    (224, ['Electronic Publishing for',
           'Physics and Astronomy'], 1997,
     ['André Heck']),

    (225, ["SCORe'96: Solar Convection",
           'and Oscillations and Their',
           'Relationship'], 1998,
     ['F. P. Pijpers', 'Jøgen Christensen-Dalsbaard', 'C. S. Rosenthal']),

    (226, ['Observational Cosmology with',
           'the New Radio Surveys'], 1998,
     ['M. N. Bremer', 'N. Jackson', 'I. Pérez-Fournon']),

    (227, ['Solar System Ices'], 1998,
     ['B. Schmitt', 'C. de Bergh', 'M. Festou']),

    (228, ['Optical Detectors for Astronomy'], 1998,
     ['James W. Beletic', 'Paola Amico']),

    (229, ['Observational Plasma Astrophysics:',
           'Five Years of Yohkoh and Beyond'], 1998,
     ['Tetsuya Watanabe', 'Takeo Kosugi', 'Alphonse C. Sterling']),

    (230, ['The Impact of Near Infrared',
           'Sky Surveys on Galactic and',
           'Extragalactic Astronomy'],
     1998, ['N. Epchtein']),

    (231, ['The Evolving Universe:',
           'Selected Topics on Large-Scale',
           'Structure and on the Properties',
           'of Galaxies'], 1998,
     ['Donald Hamilton']),

    (232, ['The Brightest Binaries'], 1998,
     ['Dany Vonbeveren', 'W. van Rensbergen', 'C. W. H. de Lorre']),

    (233, ['B[e] Stars'], 1998,
     ['Anne Marie Hubert', 'Carlos Jaschek']),

    (234, ['Observational Evindence for Black Holes',
           'in the Universe'], 1998,
     ['Sandip K. Chakrabarti']),

    (235, ['Astrophysical Plasmas and Fluids'], 1999,
     ['Vinod Krishan']),

    (236, ['Laboratory Astrophysics',
           'and Space Research'], 1998,
     ['P. Ehrenfreund', 'C. Krafft', 'H. Kochan', 'V. Pirronello']),

    (237, ['Post-Hipparcos Cosmic Candles'], 1998,
     ['André Heck', 'Filippina Caputo']),

    (238, ['Substorms-4'], 1999,
     ['S. Kokubun', 'Y. Kamide']),

    (239, ['Motions in the Solar Atmosphere'], 1999,
     ['Arnold Hanslmeier', 'Mauro Meserotti']),

    (240, ['Numerical Astrophysics'], 1999,
     ['Shoken M. Miyama', 'Kohji Tomisaka', 'Tomoyuki Hanawa']),

    (241, ['Millimeter-Wave Astronomy:',
           'Molecular Chemistry',
           'and Physics in Space'], 1999,
     ['W. F. Wall', 'Alberto Carramiñana', 'Luis Carrasco', 'P. F. Goldsmith']),

    (242, ['Cosmic Perspectives in Space Physics'], 2000,
     ['Skumar Biswas']),

    (243, ['Solar Polarization'], 1999,
     ['K. N. Nagendra', 'Jan Olof Stenflo']),

    (244, ['The Universe:',
           'Visions and Perspectives'], 2000,
     ['Naresh Dadhich', 'Ajit Kembhavi']),

    (245, ['Waves in Dusty Space Plasmas'], 2000,
     ['Frank Verheest']),

    (246, ['The Legacy of J. C. Kapteyn:',
           'Studies on Kapteyn and the',
           'Development of Modern Astrophysics'], 2000,
     ['Piet C. van der Kruit', 'Klaas van Berkel']),

    (247, ['Large Scale Structure Formation'], 2000,
     ['Reza Mansouri', 'Robert Brandenberger']),

    (248, [], None, []),
    
    (249, ['The Neutral Upper Atmosphere'], None,
     ['S. N. Gosh']),

    (250, ['Information Handling in Astronomy'], 2000,
     ['André Heck']),

    (251, ['Cosmic Plasma Physics'], 2000,
     ['Boris V. Somov']),

    (252, ['Optical Detectors in Astronomy II:',
           'State-of-the-art at the Turn',
           'of the Millennium'], 2000,
     ['Paola Amico', 'James W. Beletic']),

    (253, ['The Chemical Evolution of the Galaxy'], 2001,
     ['Francesca Matteucci']),

    (254, ['Stellar Astrophysics'], 2000,
     ['K. S. Cheng', 'Hoi Fung Chau', 'Kwing Lam Chan', 'Kam Ching Leung']),

    (255, ['The Evolution of the Milky Way:',
           'Stars versus Clusters'], 2001,
     ['Francesca Matteucci', 'Franco Giovannelli']),

    (256, ['Organizations and Strategies',
           'on Astronomy'], 2000,
     ['André Heck']),

    (257, ['Stellar Pulsation -',
           'Nonlinear Studies'], 2001,
     ['Mine Takeuti', 'Dimitar D. Sasselov']),
     
    (258, ['Electrohydrodynamics in Dusty',
           'and Dirty Plasmas:',
           'Gravito-Electrodynamics and EHD'], 2001,
     ['Hiroshi Kikuchi']),

    (259, ['The Dynamic Sun'], 2001,
     ['Arnold Hanslmeier', 'Mauro Messerotti', 'Astrid Veronig']),

    (260, ['Solar Cosmic Rays'], 2001,
     ['Leonty I. Miroshnichenko']),

    (261, ['Collisional Process in the',
           'Solar System'], 2001,
     ['Mikhail Ya. Marov', 'Hans Rickman']),

    (262, ['Whistler Phenomena',
           'Short Impulse Propogation'], 2001,
     ['Csaba Ferencz', 'Orsolya E. Ferencz', 'Dániel Hamar', 'János Lichtenberger']),

    (263, [], None, []),
    
    (264, ['The Influence of Binaries',
           'on Stellar Population Studies'], 2001,
     ['Dany Vanbeveren']),

    (265, ['Post-AGB Objects as a Phase',
           'of Stellar Evolution'], 2001,
     ['R. Szczerba', 'S. K. Góny']),

    (266, ['Organizations and Stategies',
           'in Astronomy II'], 2001,
     ['André Heck']),

    (267, ['The Nature of the Unidentified',
           'Galactic High-Energy',
           'Gamma-Ray Sources'], 2001,
     ['Al;berto Carramiñana', 'Olag Reimer', 'David J. Thompson']),

    (268, ['Multielement System Design in',
           'Astronomy and Radio Science'], 2001,
     ['Lazarus E. Koilovich', 'Leonid G. Sodin']),

    (269, ['Mechanics of Turbulence of',
           'Multicomponent Gases'], 2001,
     ['Mikhail Ya. Marov', 'Aleksander V. Kolesnichenko']),

    (270, [], None, []),

    (271, ['Astronomy-inspired Atomic',
           'and Molecular Physics'], 2002,
     ['A. R. P. Rau']),

    (272, ['Merging Processes in Galaxy Clusters'], 2002,
     ['L. Fretti', 'I. M. Gioia', 'G. Giovannini']),

    (273, ['Lunar Gavimetry'], 2002,
     ['Rune Floberghagen']),
     
]
