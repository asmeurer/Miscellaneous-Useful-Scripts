#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Modified from getben.py, which is in ~/Dowloads/comic/ as of 20080116

"""
Comics Downloader.py
Downloads comic strips from http://comics.com/ for use with the ACMEReader
program.  By default, it downloads all the strips from today to the last strip
found for each strip. The following strips are currently downloaded:
Agnes
Arlo & Janis
B.C.
Brevity
Candorville
Drabble
F Minus
Frank & Ernest
Frazz
Free Range
Geech Classics
Get Fuzzy
Off The Mark
Peanuts
Pearls Before Swine
Pickles
Reality Check
Ripley's Believe It or Not!
Wizard of Id

Command line arguments:
    -s: Download just the strips listed.  Use the ACMEReader short name (the
	name of the comic's folder in ~/Documents/Comics/).
	-t: Download strips starting with date.  It will run from that date back
	until a strip has  already been downloaded, or it is the start date for
	the strip.  The default is today (the current date)

TODO:
- Use optparser
- Fix this to work (figure out what needs to be done and do it)
- Double check the strips dict
- Clean up the source
"""

import sys
import urllib
import re
import xml.dom.minidom
import os

from string import join
from datetime import timedelta, date, datetime

# The dictionarys for the strips, all in one dictionary
strips = {
agnes : {ACMEName : 'agnes', WebName : 'agnes', FullName : 'Agnes',
    firstDate : date(2000, 9, 24)},
arlonjanis : {ACMEName : 'arlonjanis', WebName : 'arlo&janis',
    FullName : 'Arlo & Janis', firstDate : date(1996, 01, 01)},
bc : {ACMEName : 'bc', WebName : 'bc', FullName : 'B.C.',
    firstDate : date(2000, 04, 12)},
brevity : {ACMEName : 'brevity', WebName : 'brevity', FullName : 'Brevity',
    firstDate : date(2005, 01, 03)},
candorville : {ACMEName : 'candorville', WebName : 'candorvile',
    FullName : 'Candorville', firstDate : date(2003, 01, 01)},
drabble : {ACMEName : 'drabble', WebName : 'drabble', FullName : 'Drabble',
    firstDate : date(2000, 01, 01)},
fminus : {ACMEName : 'fminus', WebName : 'f_minus', FullName : 'F Minus',
    firstDate : date(2005, 05, 10)},
franknernest : {ACMEName : 'franknernest', WebName : 'frank&ernest',
    FullName : 'Frank & Ernest', firstDate : date(1996, 01, 01)}, \
frazz : {ACMEName : 'frazz', WebName : 'frazz', FullName : 'Frazz',
    firstDate : date(2001, 04, 02)},
freerange : {ACMEName : 'freerange', WebName : 'free_range',
    FullName : 'Free Range', firstDate : date(2008, 01, 13)},
geechclassics : {ACMEName : 'geechclassics', WebName : 'geech_classics',
    FullName : 'Geech Classics', firstDate : date(2000, 01, 01)},
getfuzzy : {ACMEName : 'getfuzzy', WebName : 'get_fuzzy',
    FullName : 'Get Fuzzy', firstDate : date(2000, 01, 01)},
offthemark : {ACMEName : 'offthemark', WebName : 'off_the_mark',
    FullName : 'Off the Mark', firstDate : date(2002, 09, 02)},
peanuts : {ACMEName : 'peanuts', WebName : 'peanuts', FullName : 'Peanuts',
    firstDate : date(1950, 10, 02)},
pearls : {ACMEName : 'pearls', WebName : 'pearls_before_swine',
    FullName : 'Pearls Before Swine', firstDate : date(2002, 01, 06)},
pickles : {ACMEName : 'pickles', WebName : 'pickles', FullName : 'Pickles',
    firstDate : date(2000, 01, 01)},
reality : {ACMEName : 'reality', WebName : 'reality_check',
    FullName : 'Reality Check', firstDate : date(2000, 01, 01)},
ripleys : {ACMEName : 'ripleys', WebName : 'ripleys_believe_it_or_not',
    FullName : 'Ripley\'s Believe It or Not!', firstDate : date(2000, 01, 02)},
wizardofid : {ACMEName : 'wizardofid', WebName : 'wizard_of_id',
    FullName : 'Wizard of ID', firstDate : date(2000, 01, 01)}

#path_prefix = '/Users/aaronmeurer/Documents/Comics/' + ACMEName + '/'\
	 + ACMEName + '-'
path_prefix = '/Users/aaronmeurer/Documents/Comics_test/' + ACMEName + '/'\
    + ACMEName + '-' # Testing path
# The remainder of the path with the year should be created later

# Get the command line arguments
# TODO: refactor with optparse
if len(sys.argv) > 01:
	if '-s' in sys.argv:
		while
	try:
		day = datetime.strptime(sys.argv[01], '%Y%m%d')
		day = date.fromordinal(day.toordinal())
	except ValueError, e:
		print 'The time format entered must be yyyymmdd.'
		sys.exit()
else:
	day = date.today()

pattern = re.compile('str_strip[0-9/]+\\.zoom\\.gif')
pattern2 = re.compile('str_strip[0-9/]+\\.zoom\\.jpg')
temp1 = 'http://www.comics.com/' + WebName + '/%s/'
temp2 = 'http://assets.comics.com/dyn/%s'
errornum = re.compile('404 NOT FOUND')

one_day = timedelta(01)

fileName = None

# First figure out how many days search for

if day < firstDate:
	print "There probably won't be any strips downloaded, because " \
	+ day.strftime('%Y-%m-%d') + " is before the first date, " + \
	firstDate.strftime('%Y-%m-%d')
number_of_days = 0
pathYear = str(day.year)
tempDay = day
fileNameGif = ACMEName + '-' + tempDay.strftime('%Y-%m-%d') + '.gif'
fileNameJpg = ACMEName + '-' + tempDay.strftime('%Y-%m-%d') + '.jpg'
fullPathGif = path_prefix + pathYear + '/' + fileNameGif
fullPathJpg = path_prefix + pathYear + '/' + fileNameJpg
while not os.path.exists(fullPathGif)\
	 and not os.path.exists(fullPathJpg) and tempDay >= firstDate:
	tempDay = tempDay - one_day
	number_of_days = number_of_days + 01
	pathYear = str(tempDay.year)
	fileNameGif = ACMEName + '-' + tempDay.strftime('%Y-%m-%d') + '.gif'
	fileNameJpg = ACMEName + '-' + tempDay.strftime('%Y-%m-%d') + '.jpg'
	fullPathGif = path_prefix + pathYear + '/' + fileNameGif
	fullPathJpg = path_prefix + pathYear + '/' + fileNameJpg

if number_of_days == 0:
	print FullName + ': No strips were downloaded'
else:
	print FullName + ': ' + str(number_of_days)\
		 + ' strip(s) will be downloaded (from ' + (day
			 - (number_of_days - 01) * one_day).strftime('%Y-%m-%d')\
		 + ' to ' + day.strftime('%Y-%m-%d') + ')'

# Then download the relevent strips

badDays = []
for i in range(number_of_days):
	url = temp1 % day.strftime('%Y-%m-%d')
	print '? %s: %s' % (day.strftime('%Y-%m-%d'), url)
	fil = urllib.urlopen(url)
	for line in fil:
		errorTest = errornum.search(line)
		if errorTest is not None:
			print 'Date out of range (404)'
			badDays.append(day.strftime('%Y-%m-%d'))
			break
		else:
			match = pattern.search(line)
			if match is not None:
				fileName = match.group()
				imageFormat = '.gif'
				break
			else:
				match2 = pattern2.search(line)
				if match2 is not None:
					fileName = match2.group()
					imageFormat = '.jpg'
					break
	fil.close()

	if fileName != None:
		url = temp2 % fileName
		print '+ %s: %s' % (day.strftime('%Y-%m-%d'), url)
		fil = urllib.urlopen(url)
		pathYear = str(day.year)
		if not os.path.exists(path_prefix + pathYear + '/'):
			os.mkdir(path_prefix + pathYear + '/')
			print 'Created directory: ' + path_prefix + pathYear + '/'
		fileName = ACMEName + '-' + day.strftime('%Y-%m-%d')\
			 + imageFormat
		diskfile = file(path_prefix + pathYear + '/' + fileName, 'w')
		diskfile.write(fil.read())
		fil.close()
		diskfile.close()
	else:
		print 'Image not found: ' + day.strftime('%Y-%m-%d')
		if day.strftime('%Y-%m-%d') not in badDays:
			badDays.append(day.strftime('%Y-%m-%d'))

	day = day - one_day
	fileName = None

if len(badDays) != 0:
	print 'The following dates produced errors: ' + str(badDays)

if number_of_days > len(badDays):
	print "You will now need to syncronize ACMEReader to see the new strips"
