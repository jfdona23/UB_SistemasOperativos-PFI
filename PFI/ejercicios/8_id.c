#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>

int main (void) {
    printf ("PID: %d PPID: %d UID: %d GID: %d \n", getpid(), getppid(), getuid(), getgid());
}


