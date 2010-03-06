#!/bin/sh
#############################################################################
# test_commit_range.sh - tests a range of commits in a sympy git repository.
#
# Usage: ./test_commit_range.sh earliest_commit latest_commit output_file
#
# It will start at latest_commit, run ./setup.py test and output the
# results to output_file, along with information on the SHA1 and first
# line of the commit message.  Then, it does git checkout HEAD~1 until
# it reaches earliest_commit.  Note that earliest_commit is also tested.  
#
# Note that this script does not check to see if the current directory
# is clean or indeed if it is even a sympy directory.  It also doesn't verify
# that earliest_commit is really an ancestor of latest_commit.
#
# Example:
#
# Here master is an ancestor of topic.
# $ ./test_commit_range.sh master topic output.txt
#
# SHA1 hashes work too.
# $ ./test_commit_range.sh aef2321 fe232d34 output.txt
#
# Author: Aaron Meurer
#
#############################################################################

if [$# -ne 3]
then
    echo "test_commit_range requires exactly 3 arguments."
    echo "Usage: ./test_commit_range.sh earliest_commit latest_commit output_file"
    exit 1
else
    first=$1
    last=$2
    file=$3
    git checkout $first
    while [git rev-parse $last -ne git rev-parse HEAD]
    do
        echo `git log --oneline HEAD~1..HEAD` | tee >> file
        ./setup.py test | tee >> file
    done
    exit 0
fi
