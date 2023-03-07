#ifndef __FUNCIONES_H__
#define __FUNCIONES_H__
#include <stdio.h>


#define ESCALA_TABLERO 8
#define TRUE 1
#define FALSE 0
#define ERROR -1

typedef struct Partida{
    char tablero[ESCALA_TABLERO][ESCALA_TABLERO];
    char* jugadorBlanco;
    char* jugadorNegro;
} info_tablero;

typedef struct Partido{
    char jugadas[60][3];
    int cant_jugadas;
    char turno;

}info_jugada;

int chequeo_y_juego(char* origen, char* destino);
int lectura_archivo_entrada(char* origen, info_tablero* partida, info_jugada* juego);
int leer_nombre_y_color_inicial(FILE* fp, info_tablero* partida, info_jugada* juego);
int leer_jugadas(FILE* fp, info_jugada* juego);
int jugada_validas(info_tablero* partida,info_jugada* juego, int* jugada, int* direcciones);
int validar_jugada_auxiliar(info_tablero* partida,info_jugada* juego, int* jugada, int deltax, int deltay);
int movimiento_disponible(info_tablero* partida, info_jugada* juego);
int jugada_en_rango(int* jugada);
void iniciar_tablero(info_tablero* partida);
void jugar(info_tablero* partida,info_jugada* juego, char* destino);
void mover_fichas(info_tablero* partida,info_jugada* juego, int* jugada, int* direcciones);
void transformar_jugada(char* jugada, int* jugadaTraducida);
void imprimir_tablero(info_tablero* partida);
void escribir_partida(info_tablero* partida,info_jugada* juego, char* destino);
void resultado(info_tablero* partida);
void liberar_memoria(info_tablero* partida);



#endif