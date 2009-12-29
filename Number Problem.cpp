// How many numbers are there between 1 and 1,000,000 whose sum
// of its individual digits are equal to the last two digits?
//
// Example: 512119 qualifies because 5 + 1 + 2 + 1 + 1 + 9 == 19
#include <cstdio>
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int nNumberofArgs, char* pszArgs[])
{
int numbercount;
numbercount = 0;

for (int i = 1; i <= 1000000; i++) {
	int ones;
	int tens;
	int hundreds;
	int thousands;
	int tenThousands;
	int hundredThousands;
	int millions;

	ones				= i % 10;
	tens				= i % 100 /		 10;
	hundreds			= i % 1000 /	 100;
	thousands			= i % 10000 /	 1000;
	tenThousands		= i % 100000 /	 10000;
	hundredThousands	= i % 1000000 /	 100000;
	millions			= i % 10000000 / 1000000;

	int digitsum;
	digitsum = ones + tens + hundreds + thousands + tenThousands + hundredThousands + millions;

	int lasttwodigits;
	lasttwodigits = tens * 10 + ones;


	if (digitsum == lasttwodigits) {
		cout << "\n"<< i << " works with " << digitsum << "!";
		numbercount++;
	}
	}
	cout << "\nThe number of numbers is " << numbercount << ".  \n";
    return 0;
}
