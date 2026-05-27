#include <iostream>

int main() {
    int x = 5;
    int* p = &x;
    *p = 20;

    std::cout << p;
    return 0;
}
