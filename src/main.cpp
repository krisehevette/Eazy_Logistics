#include <iostream>
#include <string>

template<typename T>
void show(const T& value) {
    std::cout << value << "\n";
}

int main() {
    show(std::string("hi"));
}
