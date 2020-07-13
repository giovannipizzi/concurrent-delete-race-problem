#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <uuid/uuid.h>
#include <errno.h>

#define MAX_SIZE 1024

int main()
{
    int i;
    int retval;
    FILE *fptr;
    struct timespec time={0,0};
    int status;
    char new_fname[MAX_SIZE];
    char uuid_string[37];
    uuid_t binuuid;

    status = mkdir("trash", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
    if (errno != EEXIST) {
        fprintf(stderr, "ERROR creating folder!\n");
        return 3;
    }

    for (i=0; i<300000; i++) {
        if( access( "DEST.txt", F_OK ) != -1 ) {
            // file exists

            uuid_generate_random(binuuid);
            uuid_unparse_lower(binuuid, uuid_string);

            strcpy(new_fname, "trash/DEST.txt-");
            strcat(new_fname, uuid_string);
            rename("DEST.txt", new_fname);

            clock_gettime(CLOCK_MONOTONIC, &time);
            printf("BE %18.10f\n", (double)time.tv_sec + 1.0e-9*time.tv_nsec);

            unlink("DEST.txt");

            clock_gettime(CLOCK_MONOTONIC, &time);
            printf("AF %18.10f\n", (double)time.tv_sec + 1.0e-9*time.tv_nsec);

        } else {
            // file doesn't exist
            printf("DEST.txt %d continue\n", i);
            usleep(1); // 1micro
        }
    }

    return 0;
}
