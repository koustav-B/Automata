#include <stdio.h>
int main() {
    int x = 0x1A;
    float y = 3.14;
    char c = 'A';
    if (x == 26) {
        /* This is a block comment
        that spans multiple lines */
        printf("Hello, World!\n");
        printf(x);
    } else {
        printf("x is not 26\n");
    }
    return 0;
}
