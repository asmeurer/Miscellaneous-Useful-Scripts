#!/usr/bin/env python3

"""Clean up the files in a folder.

This is based on an old Mac program called Folder Clean-Up, and tries to use
the same API.

All files are put into a subdirectory called _cleanup, sorted by extension.
For example, a file called "myfile.txt" would be put in "_cleanup/txts/".
Files without an extension are put in a directory called "unsorted", and
directories are put in a directory called "folders".  Note that due to the way
that os.path.splittext works, files that start with a '.' and contain only one
'.' (like ".DS_Store" or ".profile") will be put in the "unsorted" directory.
I do not know if this corresponds to the API of Folder Clean-Up.

For example:

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
|-|-|- .DS_Store
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
                    "files.", default=False) # Change this when ready to ship


args = parser.parse_args()

def main(args):
    dry_run = args.dry_run

    if dry_run:
        print("Dry run mode: None of the following operations actually occur.")
    for directory in args.directories:
        if not os.path.isdir(directory):
            print("%(file)s is not a directory." % {'file': directory}, file=sys.stderr)
            return False

    for directory in args.directories:
        print("Cleaning %(directory)s" % {'directory':directory})

        cleanup = os.path.join(directory, "_cleanup")
        if not dry_run:
            try:
                os.mkdir(cleanup)
            except OSError:
                # _cleanup directory already exists
                if not os.path.isdir(cleanup):
                    print("Could not clean %(directory)s, %(cleanup) exists and is not "
                          "a directory." % {'directory': directory, 'cleanup':
                          cleanup})
                    continue
                pass
            else:
                print("Creating cleanup directory: %(cleanup)s" % {'cleanup':
                                                                   cleanup})
        else:
            # At least check if it would give an error
            if os.path.exists(cleanup) and not os.path.isdir(cleanup):
                print("Could not clean %(directory)s, %(cleanup)s exists and is not "
                      "a directory." % {'directory': directory, 'cleanup':
                      cleanup})
                continue

        for file in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, file)):
                if file == '_cleanup':
                    continue
                ftype = 'directory'
                folder = 'folders'
            else:
                root, ext = os.path.splitext(file)
                if not ext:
                    ftype = 'extensionless file'
                    folder = 'unsorted'
                else:
                    ftype = 'file'
                    folder = ext[1:] + 's'


            newpath = os.path.join(cleanup, folder, file)

            formatd = {'ftype': ftype, 'file': os.path.join(directory, file),
                       'newpath': newpath}

            if os.path.exists(newpath):
                print("WARNING:  Could not move %(ftype)s %(file)s to "
                      "%(newpath)s/, file already exists." % formatd)
            else:
                print("Moving %(ftype)s %(file)s to %(newpath)s/" % formatd)
                if not dry_run:
                    os.renames(os.path.join(directory, file), newpath)

    return True

# XXX: This is probably not needed because of os.renames
def mkdir(path):
    """
    Wrapper to os.mkdir that does nothing if the directory already exists.
    """
    try:
        os.mkdir(path)
    except OSError:
        pass
    return path


if __name__ == '__main__':
    if main(args):
        sys.exit(0)
    else:
        sys.exit(1)
