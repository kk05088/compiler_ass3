#include <stdio.h>
#include <stdlib.h>


int sum( int y, int x)
{
    int z = y + x;
    return z;
}

char* sum( int y, int x)
{
    int z = y + x;
    char sz[5];
    return itoa(z, sz, 10);
}

int main()
{
    int a = 5;
    int b = 6;

    sum(a,b);
    printf("%d", sum(a,b));
}
