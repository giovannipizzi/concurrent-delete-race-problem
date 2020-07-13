#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h> // for usleep
#include <sys/types.h>
#include <sys/stat.h>

#define MAX_SIZE 1024

int main()
{
    int i, n, printed=0;
    char str_read[MAX_SIZE];
    char str_write[] = "CONTENT";
    int retval;
    FILE *fptr;
    struct timespec time={0,0};
    struct stat finfo;


    for (i=0; i<10000; i++) {
        clock_gettime(CLOCK_MONOTONIC, &time);
        printf("BE %18.10f\n", (double)time.tv_sec + 1.0e-9*time.tv_nsec);
        if ((fptr = fopen("DEST.txt","rb")) == NULL){
            printf(">> DELETED <<\n");
    
            usleep(1);
            // Recreate the file if it was deleted
            fptr = fopen("DEST.txt","wb");
            if(fptr == NULL)
            {
              printf("Error when re-writing file!\n");   
              return 2;
            }
            fprintf(fptr, "%s", str_write);
            fclose(fptr);
        }
        else {
            clock_gettime(CLOCK_MONOTONIC, &time);
            printf("IN %18.10f\n", (double)time.tv_sec + 1.0e-9*time.tv_nsec);

            //fgets(str_read, MAX_SIZE, fptr);
            n = read(fileno(fptr), str_read, MAX_SIZE);
            
            clock_gettime(CLOCK_MONOTONIC, &time);
            printf("AF %18.10f\n", (double)time.tv_sec + 1.0e-9*time.tv_nsec);

            usleep(1);

            retval = strcmp(str_read, str_write);
            if (retval != 0) {
                fprintf(stderr, "FOUND INSTEAD: '%s'\n", str_read);
                fstat(fileno(fptr), &finfo);
                fprintf(stderr, "ER ST_INO: %ld\n", (long int)finfo.st_ino);

                // Program exits.
                return 1;
            }
            else {
                if (printed == 0) {
                    fstat(fileno(fptr), &finfo);
                    fprintf(stderr, "OK ST_INO: %ld\n", (long int)finfo.st_ino);
                    printed = 1;
                }
            }
            fclose(fptr);
            printf("%d %s\n", i, str_read);
        }
    }

    fprintf(stderr, "READ DONE.");
    return 0;
}
