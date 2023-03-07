#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "funciones.h"

int main(int argc, char* argv[]){
    if (argc >= 3){
        return chequeo_y_juego(argv[1], argv[2]);
    }
    return ERROR;
}

