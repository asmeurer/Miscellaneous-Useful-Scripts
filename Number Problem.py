#!/usr/bin/env python3

"""
How many numbers are there between 1 and 1,000,000 whose sum of its individual
digits are equal to the last two digits?

Example: 512119 qualifies because 5 + 1 + 2 + 1 + 1 + 9 == 19

This is a literal translation of "Number Problem.cpp" in this same repo, which
I wrote a long time ago for some reason.  I've changed the variable naming
convention from CamelCase to underscores for sanity.
"""

def compute():
    numbercount = 0

    for i in range(1, 1000001):
        ones = i % 10
        tens = i % 100 // 10
        hundreds = i % 1000 // 100
        thousands = i % 10000 // 1000
        ten_thousands = i % 100000 // 10000
        hundred_thousands = i % 1000000 // 100000
        millions = i % 10000000 // 1000000

        digit_sum = (ones + tens + hundreds + thousands + ten_thousands + hundreds +
                     millions)

        last_two_digits = tens*10 + ones

        if digit_sum == last_two_digits:
            #print("%d works with %d!" % (i, digit_sum))
            numbercount += 1

    print("The number of numbers is %d." % numbercount)

compute()
compute()
