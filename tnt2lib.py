#!/usr/bin/env python2

def xor_crypt(s,mode):
	"""returns a string of encoded text"""
	sLen = len(s)
	resulttxt = []
	temp = []
	i = 0
	if(mode == 'e'):
		while i < sLen:
			temp.append(ord(s[i]) + i)
			i += 1
	if(mode == 'd'):
		while i < sLen:
			temp.append(ord(s[i]) - i)
			i += 1
	for e in temp:
		try:
			resulttxt.append(chr(e))
		except ValueError:
			pass 
	return ''.join(resulttxt)
