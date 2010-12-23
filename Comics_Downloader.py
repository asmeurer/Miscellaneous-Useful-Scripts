#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Modified from getben.py, which is in ~/Downloads/comic/ as of 20080116

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

from datetime import timedelta, date, datetime
from argparse import ArgumentParser

DATEFORMAT = '%Y-%m-%d'
# The dictionarys for the strips, all in one dictionary
strips = {
agnes : {'ACME_name':"agnes", 'web_name':"agnes", 'full_name':"Agnes",
    'first_date':date(2000, 9, 24)},
arlonjanis : {'ACME_name':"arlonjanis", 'web_name':"arlo&janis",
    'full_name':"Arlo & Janis", 'first_date':date(1996, 1, 1)},
bc : {'ACME_name':"bc", 'web_name':"bc", 'full_name':"B.C.",
    'first_date':date(2000, 4, 12)},
brevity : {'ACME_name':"brevity", 'web_name':"brevity", 'full_name':"Brevity",
    'first_date':date(2005, 1, 3)},
candorville : {'ACME_name':"candorville", 'web_name':"candorvile",
    'full_name':"Candorville", 'first_date':date(2003, 1, 1)},
drabble : {'ACME_name':"drabble", 'web_name':"drabble", 'full_name':"Drabble",
    'first_date':date(2000, 1, 1)},
fminus : {'ACME_name':"fminus", 'web_name':"f_minus", 'full_name':"F Minus",
    'first_date':date(2005, 5, 10)},
franknernest : {'ACME_name':"franknernest", 'web_name':"frank&ernest",
    'full_name':"Frank & Ernest", 'first_date':date(1996, 1, 1)}, \
frazz : {'ACME_name':"frazz", 'web_name':"frazz", 'full_name':"Frazz",
    'first_date':date(2001, 4, 2)},
freerange : {'ACME_name':"freerange", 'web_name':"free_range",
    'full_name':"Free Range", 'first_date':date(2008, 1, 13)},
geechclassics : {'ACME_name':"geechclassics", 'web_name':"geech_classics",
    'full_name':"Geech Classics", 'first_date':date(2000, 1, 1)},
getfuzzy : {'ACME_name':"getfuzzy", 'web_name':"get_fuzzy",
    'full_name':"Get Fuzzy", 'first_date':date(2000, 1, 1)},
offthemark : {'ACME_name':"offthemark", 'web_name':"off_the_mark",
    'full_name':"Off the Mark", 'first_date':date(2002, 9, 2)},
peanuts : {'ACME_name':"peanuts", 'web_name':"peanuts", 'full_name':"Peanuts",
    'first_date':date(1950, 10, 2)},
pearls : {'ACME_name':"pearls", 'web_name':"pearls_before_swine",
    'full_name':"Pearls Before Swine", 'first_date':date(2002, 1, 6)},
pickles : {'ACME_name':"pickles", 'web_name':"pickles", 'full_name':"Pickles",
    'first_date':date(2000, 1, 1)},
reality : {'ACME_name':"reality", 'web_name':"reality_check",
    'full_name':"Reality Check", 'first_date':date(2000, 1, 1)},
ripleys : {'ACME_name':"ripleys", 'web_name':"ripleys_believe_it_or_not",
    'full_name':"Ripley's Believe It or Not!", 'first_date':date(2000, 1, 2)},
wizardofid : {'ACME_name':"wizardofid", 'web_name':"wizard_of_id",
    'full_name':"Wizard of ID", 'first_date':date(2000, 1, 1)}}

#path_prefix = ''.join(["/Users/aaronmeurer/Documents/Comics/", ACME_name, "/",
#    ACME_name, "-"])
path_prefix = ''.join(["/Users/aaronmeurer/Documents/Comics_test/", ACME_name,
    "/", ACME_name, "-"]) # Testing path
# The remainder of the path with the year should be created later

# Get the command line arguments
# TODO: refactor with new optparse
usage = "usage: comics_downloader.py [-s|--strips strip names] [-t|--times dates (yyyymmdd)]"
parser = ArgumentParser(description=usage)

parser.add_option(
    '-s', '--strips',
    dest='strips',
    action='store',
    default=None,
    help="Download just the strips listed.  Use the ACMEReader short name " +
    "(the name of the comic's folder in ~/Documents/Comics/).")

parser.add_option(
    '-t', '--t',
    dest='strips',
    action='store'

if len(sys.argv) > 1:
    if '-s' in sys.argv:
#        while
        pass
    try:
        day = datetime.strptime(sys.argv[1], '%Y%m%d')
        day = date.fromordinal(day.toordinal())
    except ValueError:
        print "The time format entered must be yyyymmdd."
        sys.exit(1)
else:
    day = date.today()

pattern = re.compile('str_strip[0-9/]+\\.zoom\\.gif')
pattern2 = re.compile('str_strip[0-9/]+\\.zoom\\.jpg')
temp1 = ''.join(['http://www.comics.com/', web_name, '/%s/'])
temp2 = 'http://assets.comics.com/dyn/%s'
errornum = re.compile('404 NOT FOUND')

one_day = timedelta(1)

fileName = None

# First figure out how many days search for

if day < firstDate:
    print ''.join(["There probably won't be any strips downloaded, because ",
        day.strftime(DATEFORMAT), " is before the first date, ",
        firstDate.strftime(DATEFORMAT)])
number_of_days = 0
pathYear = str(day.year)
tempDay = day
fileNameGif = ''.join([ACME_name, "-", tempDay.strftime(DATEFORMAT), ".gif"])
fileNameJpg = ''.join([ACME_name, "-", tempDay.strftime(DATEFORMAT), ".jpg"])
fullPathGif = ''.join([path_prefix, pathYear, "/", fileNameGif])
fullPathJpg = ''.join([path_prefix, pathYear, "/", fileNameJpg])
while not os.path.exists(fullPathGif) and \
    not os.path.exists(fullPathJpg) and tempDay >= firstDate:

    tempDay = tempDay - one_day
    number_of_days = number_of_days + 1
    pathYear = str(tempDay.year)
    fileNameGif = ''.join([ACME_name, "-", tempDay.strftime(DATEFORMAT),
        ".gif"])
    fileNameJpg = ''.join([ACME_name, "-", tempDay.strftime(DATEFORMAT),
        ".jpg"])
    fullPathGif = ''.join([path_prefix, pathYear, "/", fileNameGif])
    fullPathJpg = ''.join([path_prefix, pathYear, "/", fileNameJpg])

if number_of_days == 0:
    print ''.join([FullName, ": No strips were downloaded"])
else:
    print ''.join([FullName, ": ", str(number_of_days), " strip(s) will",
        "be downloaded (from ", (day - (number_of_days -
        1)*one_day).strftime(DATEFORMAT), " to ",
        day.strftime(DATEFORMAT), ")"])

# Then download the relevent strips

badDays = []
for i in range(number_of_days):
    url = temp1 % day.strftime(DATEFORMAT)
    print "? %s: %s" % (day.strftime(DATEFORMAT), url)
    fil = urllib.urlopen(url)
    for line in fil:
        errorTest = errornum.search(line)
        if errorTest is not None:
            print "Date out of range (404)"
            badDays.append(day.strftime(DATEFORMAT))
            break
        else:
            match = pattern.search(line)
            if match is not None:
                fileName = match.group()
                imageFormat = ".gif"
                break
            else:
                match2 = pattern2.search(line)
                if match2 is not None:
                    fileName = match2.group()
                    imageFormat = ".jpg"
                    break
    fil.close()

    if fileName != None:
        url = temp2 % fileName
        print "+ %s: %s" % (day.strftime(DATEFORMAT), url)
        fil = urllib.urlopen(url)
        pathYear = str(day.year)
        if not os.path.exists(''.join([path_prefix, pathYear, "/"])):
            os.mkdir(''.join([path_prefix, pathYear, "/"]))
            print ''.join(["Created directory: ", path_prefix, pathYear, "/"])
        fileName = ''.join([ACME_name, "-", day.strftime(DATEFORMAT),
            imageFormat])
        diskfile = file(''.join([path_prefix, pathYear, "/", fileName, 'w']))
        diskfile.write(fil.read())
        fil.close()
        diskfile.close()
    else:
        print ''.join(["Image not found: ", day.strftime(DATEFORMAT)])
        if day.strftime(DATEFORMAT) not in badDays:
            badDays.append(day.strftime(DATEFORMAT))

    day = day - one_day
    fileName = None

if badDays:
    print "The following dates produced errors:"
    print badDays

if number_of_days > len(badDays):
    print "You will now need to syncronize ACMEReader to see the new strips"
