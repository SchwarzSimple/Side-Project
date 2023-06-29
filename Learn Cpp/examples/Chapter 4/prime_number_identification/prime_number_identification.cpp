#include <iostream>

bool isPrime(int x)
{
	return (x == 2 || x == 3 || x == 5 || x == 7);
}

int main()
{
	std::cout << "Enter a number 0 through 9: ";
	int x{};
	std::cin >> x;

	if ( isPrime(x))
		std::cout << "The digit is a prime\n";
	else
		std::cout << "The digit is not a prime\n";

	return 0;
}