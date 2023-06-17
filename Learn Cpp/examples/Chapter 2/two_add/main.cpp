#include "io.h"

int main()
{
	int num_one{ readNumber() };
	int num_two{ readNumber() };
	writeAnswer(num_one + num_two);

	return 0;
}