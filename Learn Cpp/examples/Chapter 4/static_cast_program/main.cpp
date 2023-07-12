#include <cstdint>
#include <iostream>

int main()
{
    std::cout << "Enter a single chracter: ";
    char ch{};
    std::cin >> ch;

    std::cout << "You entered '" << ch << "', which has ASCII code "<< static_cast<int>(ch) << "." << '\n';

    return 0;
}
