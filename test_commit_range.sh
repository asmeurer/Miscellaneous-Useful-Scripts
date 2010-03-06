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

if [ $# -ne 3 ]
then
    echo "test_commit_range.sh requires exactly 3 arguments."
    echo "Usage: ./test_commit_range.sh earliest_commit latest_commit output_file"
    echo *
    exit 1
else
    # If we start on a branch, we want to end there too
    currentbranch=`git branch | grep '^\*' | sed 's/\* \(.*\)/\1/g'`
    if [ "$currentbranch" != "(no branch)" ]
    then
        current=$currentbranch
    else
        current=`git rev-parse HEAD`
    fi
    first=`git rev-parse $1~1`
    last=`git rev-parse $2`
    file=$3
    git checkout -q $last
    while [ `git rev-parse $first` != `git rev-parse HEAD` ]
    do
        echo Moving to `git log --oneline | head -n 1` | tee -a $file
        ./setup.py test | tee -a $file
        echo | $file
        git checkout -q HEAD~1
    done
    git checkout -q $current
    exit 0
fi
