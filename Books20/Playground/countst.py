#! /usr/bin/env python

year = 1960
volume = 19
for page in range(1, 4):
    for volume in range(volume, volume+28, 2):
        print('Vol. {} {}                         Vol. {} {}'.format(volume, year, volume+28, year+14))
        print('    Jan Feb Mar Apr May Jun            Jan Feb Mar Apr May Jun')
        print('Vol. {} {}                         Vol. {} {}'.format(volume+1, year, volume+29, year+14))
        print('    Jul Aug Sep Oct Nov Dec            Jul Aug Sep Oct Nov Dec\n')
        year += 1

    print('')
    year += 14
    volume += 30
