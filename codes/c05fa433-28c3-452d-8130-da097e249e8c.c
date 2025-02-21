#include <stdio.h>

int main() {
    int num;

    // Prompt user for input
    printf("Enter a number: ");
    fflush(stdout);  // Flush output before taking input

    // Take input
    scanf("%d", &num);

    // Print output
    printf("You entered: %d\n", num);

    return 0;
}