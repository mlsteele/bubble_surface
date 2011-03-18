#! /usr/bin/env python2.7

import pstats

def main():
	p = pstats.Stats('profile')
	
	p.strip_dirs()
	p.sort_stats('cumulative')
	
	p.print_stats(15)

if __name__ == '__main__':
    main()