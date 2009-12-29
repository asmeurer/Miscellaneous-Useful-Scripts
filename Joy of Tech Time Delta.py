#!/usr/bin/env python
#
#  Joy of Tech Time Delta.py
#
#
#  Created by Aaron Meurer on 4/18/09.
#
"""
Changes the file names in the directory given in the command line arguments from
date offsets from the unix epoch (19700101), with thejoyoftech appended and
formatted for ACMEReader.

Usage:
python Joy\ of\ Tech\ Time\ Delta.py /path/to/directory/of/images/
"""
from datetime import timedelta, date
from sys import argv
from os import rename, chdir, walk
from os.path import splitext, join

e = date(1970,1,1)

def formatNum(filename):
    filename = splitext(filename)
    day = e + timedelta(int(filename[0]))
    return day.strftime("thejoyoftech100--%Y-%m-%d") + filename[1]

try:
    for files in walk(argv[1]):
        for i in files[2]:
            if i != ".DS_Store":
                try:
                    newname = formatNum(i)
                    rename(join(files[0],i),join(files[0],newname))
                except ValueError:
                    print "Could not change file:", i
                else:
                    print i," -> ", newname
except OSError:
    print "Could not open ", argv[1]
