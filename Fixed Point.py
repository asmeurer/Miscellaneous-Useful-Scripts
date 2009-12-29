#!/usr/local/bin/python
#
#  Fixed Point.py
#
#
#
from math import *
x = .5
while x ** x != x:
	print "%.25f" % (x ** x)
	x = x ** x
