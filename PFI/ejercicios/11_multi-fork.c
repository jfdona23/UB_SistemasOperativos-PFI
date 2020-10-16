#include <stdio.h> 
#include <sys/types.h>
#include <unistd.h>

void showID() {
    printf ("I´m the child: %d and my parent is : %d \n", getpid(), getppid());
    sleep(5);
}

int main(void) {
	pid_t pid1, pid2, pid3, pid4;
	pid1 = fork();
    if (pid1 == 0) {
        showID();
        pid3 = fork();
        if (pid3 == 0) { showID(); }
    } else {
        pid2 = fork();
        if (pid2 == 0) {
            showID();
            pid4 = fork();
        if (pid4 == 0) { showID(); }
        } else {
            printf ("Soy el proceso principal: %d \n", getpid());
        }
    }
    sleep(1);
}

