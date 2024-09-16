#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define RAND_MAX 0x7fffffff

__extension__ unsigned long long _rand_next = 0;

void VIPsrand(unsigned int seed)
{
    _rand_next = seed;
}

int VIPrand(void)
{
    _rand_next = _rand_next * __extension__ 6364136223846793005LL + 1;
    return (int)(_rand_next >> 32) & RAND_MAX;
}
int main() {
    unsigned int arr[32];          
    unsigned char flag[32];         
    unsigned int arr_1[256];       
    unsigned int arr_256[256];          
    // unsigned int *arr_2561;
    int i, j, a, b, x, y;
    
    memcpy(flag, "ptm{REDACTEDREDACTEDREDACTEDRED}", 0x21);
    i=0;
    if (i == 0) {
        y = 0;
        VIPsrand(1);
        for (i = 0; i < 32; i++) {
            arr[i] = (unsigned char)i;
        }

        for (i = 0; i < 256; i++) {
            arr_1[i] = i;
        }

        i = 1337;
        do {
            for (j = 1000; j > 0; j--) {
                a = VIPrand();
                b = VIPrand();
                if ((a % 32) != (b % 32)) {
                    x = a % 32;
                    y = b % 32;

                    unsigned int temp = arr[x];
                    arr[x] = arr[y];
                    arr[y] = temp;
                }
            }

            for (j = 10000; j > 0; j--) {
                y = VIPrand() & 0xff;
                x = VIPrand() & 0xff;

                if (y != x) {
                    unsigned int temp = arr_1[x];
                    arr_1[x] = arr_1[y];
                    arr_1[y] = temp;
                }
            }
            
            for (j = 0; j < 32; j++) {
                arr_256[j] = flag[arr[j]];
                // printf("%d, ",flag[])
            }

            for (j = 0; j < 32; j++) {
                flag[j] = arr_256[arr[j]];
            }


            for (j = 0; j < 32; j++) {
                flag[j] = arr_1[flag[j]];
            }

            for (j = 0; j < 32; j++) {
                flag[j] ^= (unsigned char)VIPrand();
            }

            i--;
        } while (i > 0);
        
        for (i = 0; i < 32; i++) {
            for (j = 0; j < 256; j++) {
                arr_256[j] = (arr_256[j]<<1);
            }
            arr_256[flag[i]] ^= 1;
        }

        putchar('\n');
        for (i = 0; i < 16; i++) {
            unsigned int sum = 0;
            for (j = 0; j < 16; j++) {
                sum += arr_256[i*0x10+j];
            }
            printf("%u, ", sum);
        }
        putchar('\n');

        for (i = 0; i < 16; i++) {
            unsigned int sum = 0;
            for (j = 0; j < 16; j++) {
                sum += arr_256[i + j*0x10];
            }
            printf("%u, ", sum);
        }
        putchar('\n');

    }

    return 0;
}
