#!/usr/bin/env python3

# XXX: Don't put a newline here, or it will add an extra line with
# folder_cleanup.py --help
#  |
#  v
"""Clean up the files in a folder.

This is based on an old Mac program called Folder Clean-Up.

All files are put into a subdirectory called _cleanup, sorted by extension.
For example, a file called "myfile.txt" would be put in "_cleanup/txts/".
Files without an extension are put in a directory called "unsorted", and
directories are put in a directory called "folders".  For example:

YourFolder:
|- _cleanup:
|-|- avis:
|-|-|- sound.avi
|-|- folders:
|-|-|- a_directory:
|-|-|-|- stuff.txt
|-|- txts:
|-|-|- myfile.txt
|-|- unsorted:
|-|-|- noextension

Run like

$ python3 folder_cleanup.py Directory_to_clean/

"""
import sys

# This file contains syntax that isn't Python 2 compatible anyway
# if sys.version[0] < '3':
#     print("This script requires Python 3")
#     sys.exit(1)

import argparse
import os

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("directories", nargs='+', help="The directories to be cleaned.")

parser.add_argument("--dry-run", "-d", dest="dry_run", action="store_true",
                    help="Print what would happen, but don't actually move the "
                    "files.", default=True) # Change this when ready to ship


args = parser.parse_args()

for file in args.directories:
    if not os.path.isdir(file):
        print("%(file)s is not a directory." % {'file': file}, file=sys.stderr)
        sys.exit(1)
