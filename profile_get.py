#! /usr/bin/env python2.7

import subprocess

def main():
	print "Collecting profile -> profile"
	subprocess.call(
		"python2.7 -m cProfile -o profile amoeba1.py",
		shell=True
	)
	
	print "Profile Collected -> profile"

if __name__ == '__main__':
    main()