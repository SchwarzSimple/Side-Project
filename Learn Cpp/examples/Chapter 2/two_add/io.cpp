#include "io.h"
#include <iostream>

int readNumber()
{
	std::cout << "Enter an interger: ";
	int input{};
	std::cin >> input;

	return input;
}

void writeAnswer(int x)
{
	std::cout << "The sum of two integers: " << x << '\n';
}