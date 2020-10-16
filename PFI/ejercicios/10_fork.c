#include <stdio.h> 
#include <sys/types.h>
#include <unistd.h>

int main(void) {
	pid_t pid;
	printf ("Just one process so far \nCalling fork ....\n");
	pid = fork();
	if ( pid == 0 ) {
		printf ("I´m the child: %d and my parent is : %d \n", getpid(), getppid());
	} else if ( pid > 0 ) {
		printf ("I´m the parent: %d and my child is: %d \n", getpid(), pid);
	} else
		printf ("fork returned error code, no child \n");
}