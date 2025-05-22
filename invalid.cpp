#include<iostream>

int main() {
    int n;
    std::cin >> n;
    int a[n];
    for (int i = 0; i < n; i++) {
        std::cin >> a[i]
    }
    int ans = 0;
    for (int i = 0; i < n; i++) {
        ans ^= a[i];
    }
    std::cout << ans << std::endl;
}