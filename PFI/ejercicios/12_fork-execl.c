#include <stdio.h>
#include <stdlib.h>
#include<sys/wait.h>
#include<sys/types.h>
#include <unistd.h>

void fatal (char *s) ;

int main (void) {
    pid_t pid;
    int status;
    pid = fork();
    if ( pid == 0 ) {
        execl ("/bin/ls", "ls", "-l", NULL);
        fatal ("execl failed");
    } else if ( pid > 0 ) {
        wait(&status);
        printf ("ls completed\n" );
    } else
        fatal ("fork failed");
    }

void fatal (char *s) {
    perror (s);
    exit (1);
}

