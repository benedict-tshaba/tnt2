#!/usr/bin/env python2

# Tnt2 is a re-write of my previous program Tnt. It is a simple note-taking
# program which I use to take class notes and write simple reminders.
# Copyright (C) 2017  Tshaba Phomolo Benedict

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
