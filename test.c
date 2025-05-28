#include <stdio.h>
#include <string.h>
#include "minu.h";

typedef struct {
    char name[32];
    int age;
} User;

void greet(const char* name) {
    printf("Welcome, %s!\n", name);
}

int main() {
    printf("Hello, C syntax check!\n");

    User user;
    strcpy(user.name, "Hayannoon");
    user.age = 29;
    printf("User: %s, Age: %d\n", user.name, user.age);

    int numbers[] = {1, 2, 3, 4, 5};
    printf("Doubled numbers: ");
    for (int i = 0; i < 5; ++i) {
        printf("%d ", numbers[i] * 2);
    }
    printf("\n");

    greet("C");
    greet("C");
    greet("C");

    return 0;
}