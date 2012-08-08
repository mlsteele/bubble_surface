# python 2.7

import pstats

p = pstats.Stats('profile_data')
p.strip_dirs()
p.sort_stats('cumulative')
p.print_stats(25)
