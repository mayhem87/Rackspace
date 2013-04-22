#!/usr/bin/env python

import string
import sys

self, word, dist = sys.argv

letters = {}

for x, y in enumerate(string.ascii_letters):
	letters[y] = x

def rotator(word, dist):
	newword = ''
	for x in word:
		number = letters[x] + dist
		newword += string.ascii_letters[number]
	print newword

if __name__ == '__main__':
	rotator(word,int(dist))

