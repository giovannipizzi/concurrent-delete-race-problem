#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

int main()
{
    int i;
    FILE *fptr;
    struct timespec time={0,0};

    for (i=0; i<3000000; i++) {
        if( access( "DEST.txt", F_OK ) != -1 ) {
            // file exists
            usleep(1);
            
            clock_gettime(CLOCK_MONOTONIC, &time);
            printf("BE %18.10f\n", (double)time.tv_sec + 1.0e-9*time.tv_nsec);

            unlink("DEST.txt");

            clock_gettime(CLOCK_MONOTONIC, &time);
            printf("AF %18.10f\n", (double)time.tv_sec + 1.0e-9*time.tv_nsec);
        } else {
            // file doesn't exist
            printf("DEST.txt %d continue\n", i);
            usleep(1);
        }
    }

    fprintf(stderr, "DELETE DONE.");
    return 0;
}
