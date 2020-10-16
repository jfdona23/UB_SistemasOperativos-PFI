#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int salirConError() {
    printf("Parametro ingresado incorrecto\n");
    exit(1);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        salirConError();
    }
    int statusCode = atoi(argv[1]);
    if (statusCode >= 0 && statusCode <= 255) {
        exit(statusCode);
    } else {
        salirConError();
    }
}

