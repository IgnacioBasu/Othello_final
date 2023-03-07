#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "funciones.h"

// Cabe aclarar que siempre que se mencionan las estructuras son info_tablero o info_jugada
// segun lo necesite la funcion.

/*
Esta función recibe como argumentos dos strings que representan los nombres de 
dos archivos de texto. Luego lee los datos contenidos en el archivo de 
origen y ejecuta el juego Othello. Por resultado del juego se escribe en el 
archivo de destino (solo si la partida quedo incompleta) o se muestra lo 
sucedido (ganador,empate,error de jugada).
Caso que suceda algun problema la funcion nos retorna -1, que indica error.
*/
int chequeo_y_juego(char* origen, char* destino){
    info_tablero partida;
    info_jugada juego;

    iniciar_tablero(&partida);

    if  (lectura_archivo_entrada(origen, &partida, &juego)==-1) return ERROR; 
    
    jugar(&partida, &juego, destino);
    liberar_memoria(&partida);
    return 0;
}

/*
Esta función recibe como argumentos un string que representa el nombre del archivo
de entrada y dos punteros a estructuras, en las que se guardan la data del partido 
La función lee los datos contenidos en el archivo y guarda la información en las 
estructuras con el uso de leer_nombre_y_color_inicial y leer_jugadas.
Caso que suceda algun problema la funcion nos retorna -1, que indica error.
*/
int lectura_archivo_entrada(char* origen, info_tablero* partida, info_jugada* juego){
    FILE* fp;
    int nombre_y_color_correctos = TRUE;
    int jugadas_correctas = TRUE;

    fp = fopen(origen, "r");
    if(fp == NULL) {
      printf("No se pudo abrir el archivo\n");
      return ERROR;
    }
 
    nombre_y_color_correctos = leer_nombre_y_color_inicial(fp, partida, juego);
    jugadas_correctas = leer_jugadas(fp, juego);
    if (!nombre_y_color_correctos && !jugadas_correctas) return ERROR;

    fclose(fp);

    return 0;
}

/*
Esta función recibe como argumentos un puntero a un archivo de texto y a dos estructuras.
La función lee el nombre y el color del jugador que comienza la partida y 
guarda la información relevante en las estructuras planteadas (info_tablero e
info_jugada.).
Caso que suceda algun problema la funcion nos retorna FALSE, que indica que hubo
fallas. De lo contrario nos retorna TRUE.
*/
int leer_nombre_y_color_inicial(FILE* fp, info_tablero* partida, info_jugada* juego) {
    partida->jugadorBlanco = NULL;
    partida->jugadorNegro = NULL;
    char nombre[100], color = ' ', line[100], color_inicial = '\0';
    int cantidad_de_argumentos = 0, i = 0, cantidad_de_jugadores = 2 ;

    for (int i = 0; i < cantidad_de_jugadores; i++) {
        if (fscanf(fp, "%99[^,\n],%c", nombre, &color) == 2) {
            while (fgetc(fp) != '\n') {} // Descartar el resto de la línea

            if (color == 'B' && !partida->jugadorBlanco) {
                partida->jugadorBlanco = strdup(nombre);
                cantidad_de_argumentos++;
            } else if (color == 'N' && !partida->jugadorNegro) {
                partida->jugadorNegro = strdup(nombre);
                cantidad_de_argumentos++;
            }
        }
    }

    if (cantidad_de_argumentos != cantidad_de_jugadores) {
        printf("Error de formato: no se encontraron ambos nombres de los jugadores.\n");
        return FALSE;
    }

    if (fgets(line, sizeof(line), fp) == NULL) {
        printf("Error de formato: no se puede leer el color que le toca jugar.\n");
        return FALSE;
    }



    while (line[i] == ' ' || line[i] == '\t' || line[i] == '\n' || line[i] == '\r') {
        i++;
    }

    if (line[i] == '\0') {
        printf("Error de formato: la linea que debe tener el jugador que juega esta vacia.\n");
        return FALSE;
    }

    color_inicial = line[i];

    if (color_inicial != 'B' && color_inicial != 'N') {
        printf("Error de formato: el color inicial: (%c) es invalido.\n", color_inicial);
        return FALSE;
    }

    juego->turno = color_inicial;

    return TRUE;
}

/*
Esta función recibe como argumentos un puntero a un archivo de texto y a una 
estructura. La función lee las jugadas del archivo y guarda la información en la
estructura correspondiente.
*/
int leer_jugadas(FILE* fp, info_jugada* juego) {
    juego->cant_jugadas = 0;
    char buffer[60 + 1];
    int i = 0;
    while (fgets(buffer, sizeof(buffer), fp) != NULL && juego->cant_jugadas < 60) {
        // Eliminar el carácter de nueva línea al final
        for (i = 0; buffer[i] != '\n' && buffer[i] != '\0'; i++);
        buffer[i] = '\0';
        // Copiar la línea al array jugadas
        strncpy(juego->jugadas[juego->cant_jugadas], buffer, 3);
        // Incrementar cant_jugadas
        juego->cant_jugadas++;
    }
    return (juego->cant_jugadas > 0);
}

/* Esta función es la principal.
En caso de ser una jugada válida, se llama a la función mover_fichas para 
realizar la jugada. 
Si la jugada no es válida, se marca la partida como terminada y se imprime un 
mensaje de error.
Si se intenta saltar el turno, se verifica si hay movimientos disponibles y si
no se ha intentado saltar el turno en la jugada anterior. Si se intenta saltar
el turno dos veces seguidas, la partida termina.
Luego si todas las jugadas fueron realizadas o la partida se termino, 
se verifica quién es el ganador y se escribe el resultado en el archivo de destino.
*/
void jugar(info_tablero* partida,info_jugada* juego,char* destino){
    int continuar = FALSE, direcciones[8], jugada_valida = 0, jugada[2];
    int i = 0, pre_salto_turno = FALSE;
    while (i < juego->cant_jugadas && !continuar) {
        if (juego->jugadas[i][0] != '\0') { 
            pre_salto_turno = FALSE;
            transformar_jugada(juego->jugadas[i], jugada);
            jugada_valida = jugada_validas(partida, juego, jugada, direcciones);
            if (jugada_valida) {
                mover_fichas(partida, juego, jugada, direcciones);
            }
        }
        else { 
            jugada_valida = TRUE;
            if (movimiento_disponible(partida, juego)) {
                printf("Hay movimientos disponibles, no se puede salteaer el turno\n");
                jugada_valida = FALSE;
            }
            if (pre_salto_turno && jugada_valida) { 
                continuar = TRUE;
            }
            pre_salto_turno = TRUE;
        }
        if (!jugada_valida) {
            continuar = TRUE;
            if (juego->turno == 'B') {
                printf("La jugada es invalida: (%s)\n", juego->jugadas[i]);
            }
            else {
                printf("La jugada es invalida: (%s)\n", juego->jugadas[i]);
            }
            imprimir_tablero(partida);
        }
        juego->turno = (juego->turno == 'B') ? 'N' : 'B';
        i++;
    }
    if (jugada_valida) {
        continuar = !movimiento_disponible(partida, juego);
        if (continuar) {
            juego->turno = (juego->turno == 'B') ? 'N' : 'B';
            continuar = !movimiento_disponible(partida, juego);
            juego->turno = (juego->turno == 'B') ? 'N' : 'B';
        }
        if (!continuar) {
            escribir_partida(partida,juego,destino);
        }
        else {
            resultado(partida);
        }
    }
}

/*
Esta función recibe como argumentos dos punteros a estructuras y dos arreglos de
enteros. La función verifica si una jugada es válida en el juego Othello y retorna un
valor TRUE o FALSE. Además, guarda las direcciones en las que se deben 
voltear las fichas en el arreglo de direcciones.
*/
int jugada_validas(info_tablero* partida,info_jugada* juego, int* jugada, int* direcciones) {
    int  ficha_contigua[2], direccion = 0, jugada_valida = FALSE, cambios = FALSE;
    int DIRECCIONES[8][2] = {{-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}};

    if (!jugada_en_rango(jugada)) return FALSE;
    if (partida->tablero[jugada[1]][jugada[0]] != 'X') return FALSE;

    for (int x = 0; x < 8; x++) {
        ficha_contigua[0] = jugada[0] + DIRECCIONES[x][0];
        ficha_contigua[1] = jugada[1] + DIRECCIONES[x][1];
        if (!jugada_en_rango(ficha_contigua) || partida->tablero[ficha_contigua[1]][ficha_contigua[0]] == 'X' || partida->tablero[ficha_contigua[1]][ficha_contigua[0]] == juego->turno) {
            direcciones[direccion] = 0;
            direccion++;
            continue;
        }
        cambios = validar_jugada_auxiliar(partida, juego, jugada, DIRECCIONES[x][0], DIRECCIONES[x][1]);
        direcciones[direccion] = cambios;
        direccion++;
        if (!jugada_valida && cambios != 0) jugada_valida = TRUE;
    }

    return jugada_valida;
}

/*
Esta función recibe como argumentos dos punteros a estructuras, un puntero a un 
arreglo de enteros que representa una jugada y dos enteros que representan una 
dirección en la que se  debe voltear una ficha. La función verifica si se puede
voltear una ficha en la dirección dada y retorna TRUE o FALSE.
*/
int validar_jugada_auxiliar(info_tablero* partida, info_jugada* juego, int* jugada, int deltax, int deltay) {
    int ficha_contigua[2] = {jugada[0] + deltax, jugada[1] + deltay}, cambios = 0;
    char color_adyacente;

    while (jugada_en_rango(ficha_contigua)) {
        color_adyacente = partida->tablero[ficha_contigua[1]][ficha_contigua[0]];
        if (color_adyacente == juego->turno) {
            return cambios;
        } else if (color_adyacente == 'X') {
            return 0;
        }
        cambios++;
        ficha_contigua[0] += deltax;
        ficha_contigua[1] += deltay;
    }

    return 0;
}

/*
Esta función recibe dos punteros a estructuras,un puntero a un arreglo de enteros
y un puntero a un arreglo de enteros.
La función se utiliza para mover una ficha en el tablero en la posición especificada
por el arreglo "jugada" y en las direcciones especificadas por el arreglo "direcciones".
*/
void mover_fichas(info_tablero* partida,info_jugada* juego, int* jugada, int* direcciones){
    int DIRECCIONES[8][2] = {{-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}};
    int ficha_contigua[2];
    
    ficha_contigua[0] = jugada[0];
    ficha_contigua[1] = jugada[1];

    partida->tablero[jugada[1]][jugada[0]] = juego->turno;

    for (int x = 0; x < 8; x++) {
        for (int cambios = 0; cambios < direcciones[x]; cambios++) {
            ficha_contigua[0] += DIRECCIONES[x][0];
            ficha_contigua[1] += DIRECCIONES[x][1];
            partida->tablero[ficha_contigua[1]][ficha_contigua[0]] = juego->turno;
        }
        ficha_contigua[0] = jugada[0];
        ficha_contigua[1] = jugada[1];
    }
}

/*
Esta función recibe como argumento un puntero a un arreglo de enteros que representa
 una jugada. Luego verifica si la jugada está dentro del rango válido nos retorna
TRUE o FALSE segun este o no la jugada en el rango permitido.
*/
int jugada_en_rango(int* casilla) {
    int x = casilla[0];
    int y = casilla[1];
    return (x >= 0 && x < ESCALA_TABLERO && y >= 0 && y < ESCALA_TABLERO);
}

/*
Esta función recibe como argumento un string y puntero a un arreglo de enteros que 
representa una  jugada. Luego verifica si la jugada está dentro del rango válido
 y nos "retorna" la jugada pasada a un sistema (x, y)
*/
void transformar_jugada(char* jugada, int* jugadaTraducida){
    jugadaTraducida[0] = (int)(toupper(jugada[0]))-'A';
    jugadaTraducida[1] = (int)((jugada[1])-'0')-1;
}

/*
Esta función recibe dos punteros a estructuras. Luego retorna TRUE o FALSE
indicando si hay un movimiento disponible en el tablero para el jugador actual.
*/
int movimiento_disponible(info_tablero* partida, info_jugada* juego){
    int jugada[2], continuar= TRUE, direcciones[8];

    while (continuar)
    {
    for(int fila=0; fila < ESCALA_TABLERO; fila++){
        for(int columna=0; columna < ESCALA_TABLERO ; columna++){
            if (partida->tablero[fila][columna]=='X'){
                jugada[0] = columna;
                jugada[1] = fila;
                continuar = jugada_validas(partida,juego, jugada, direcciones);
            }
        }
    }
    return TRUE;
    }
    return FALSE;
}

/*
Esta función recibe un puntero a  la estructura. Luego recorriendo el tablero, lo
imprime y le agrega cierto estilo para la impresion del mismo.
*/
void imprimir_tablero(info_tablero* partida){
    printf("\n     A  B  C  D  E  F  G  H\n");
    printf("     -  -  -  -  -  -  -  -\n");
    for (int i = 0; i < 8; i++) {
        printf("%d | ", i + 1);
        for (int j = 0; j < 8; j++) {
            printf(" %c ", partida->tablero[i][j]);
        }
         printf("| %d\n", i + 1);
     }
     printf("     -  -  -  -  -  -  -  -\n");
    printf("     A  B  C  D  E  F  G  H\n");
}

/*
Esta función recibe dos punteros a estructuras y un puntero a una cadena de 
caracteres que representa el nombre del archivo de destino. 
La función se utiliza para escribir la información de una partida de Othello
en un archivo de texto.
*/
void escribir_partida(info_tablero* partida,info_jugada* juego, char* destino){
    FILE* fp;
    fp = fopen(destino, "w");

    for(int fila = 0; fila < ESCALA_TABLERO; fila++){
        for(int columna = 0; columna < ESCALA_TABLERO; columna++){
            fprintf(fp, "%c", partida->tablero[fila][columna]);
        }
        fprintf(fp, "\n");
    }
    fprintf(fp, "%c\n", juego->turno);

    fclose(fp);
}

/*
Esta función recibe como argumentos un puntero a estructura en la que se encuentra
el tablero actual. Luego recorre dicho tablero y cuenta las fichas de cada jugador 
para determinar la situacion final de la partida.
*/
void resultado(info_tablero* partida){
    int fichas_blancas = 0, fichas_negras = 0;
    for(int i = 0; i < (ESCALA_TABLERO * ESCALA_TABLERO); i++){
        if (partida->tablero[i/8][i%8] == 'B') fichas_blancas++;
        else if (partida->tablero[i/8][i%8] =='N') fichas_negras++;
    }
    if (fichas_blancas > fichas_negras){
        printf("El ganador es %s con %d, mientras que el otro jugador tiene %d)\n", partida->jugadorBlanco, fichas_blancas, fichas_negras);
    }
    else if(fichas_negras > fichas_blancas){
        printf("El ganador es %s con %d, mientras que el otro jugador tiene %d)\n", partida->jugadorNegro, fichas_negras, fichas_blancas);
    }
    else{
        printf("Empate con %d\n", fichas_blancas);
    }

}

/*
Esta función inicializa el tablero del juego Othello. En ella se colocan las 4
fichas principales y para espacio vacio una 'X'.
*/
void iniciar_tablero(info_tablero* partida){
    for(int fila = 0; fila < ESCALA_TABLERO; fila++){
        for(int columna = 0; columna < ESCALA_TABLERO; columna++){
            partida->tablero[fila][columna] = 'X';
        }
    }
    partida->tablero[3][3] = 'B';
    partida->tablero[3][4] = 'N';
    partida->tablero[4][3] = 'N';
    partida->tablero[4][4] = 'B';

}

/*
Esta función libera memoria a los dos punteros de la escrutura info_tablero.
*/
void liberar_memoria(info_tablero* partida){
    free(partida->jugadorBlanco);
    free(partida->jugadorNegro);
}