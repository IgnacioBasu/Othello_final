#include "tests.h"

int main(){
    test_chequeo_y_juego();

    test_lectura_archivo_entrada();

    test_leer_nombre_y_color_inicial();
    
    test_jugada_valida();

    test_validar_jugada_auxiliar();

    test_jugada_en_rango();

    test_movimiento_disponible();

    printf("------------------------------------------------------");
    printf("\n Los testeos de funciones fueron pasados con exito \n");
    printf("------------------------------------------------------");
    return 0;
}

// Los archivos tablero son archivos vacios
// El archivo prueba esta en un formato correcto
// El archivo prueba_2 esta vacio
void test_chequeo_y_juego(){
    assert(chequeo_y_juego("./recursos/prueba.txt", "./recursos/tablero.txt")==0);
    assert(chequeo_y_juego("./recursos/prueba_2.txt", "./recursos/tablero.txt")==-1);
}

void test_lectura_archivo_entrada(){
    info_tablero partida;
    info_jugada juego;

    iniciar_tablero(&partida);
    assert(lectura_archivo_entrada("./recursos/prueba.txt", &partida,&juego)==0);
    liberar_memoria(&partida);


    iniciar_tablero(&partida);
    assert(lectura_archivo_entrada("./recursos/prueba_2.txt", &partida,&juego)==-1);
    liberar_memoria(&partida);
}

void test_leer_nombre_y_color_inicial(){
    info_tablero partida;
    info_jugada juego;
    FILE* fp;

    iniciar_tablero(&partida);
    
    fp = fopen("./recursos/prueba.txt", "r"); // El formato es correcto
    assert(leer_nombre_y_color_inicial(fp, &partida, &juego) == TRUE);
    fclose(fp);
    liberar_memoria(&partida);

    iniciar_tablero(&partida);
    
    fp = fopen("./recursos/prueba_3.txt", "r"); // No estan los nombres bien
    assert(leer_nombre_y_color_inicial(fp, &partida, &juego) == FALSE);
    fclose(fp);
    liberar_memoria(&partida);
}

void test_leer_jugadas(){
    info_jugada juego;
    info_tablero partida;
    FILE* fp;

    iniciar_tablero(&partida);

    fp = fopen("./recursos/terminada.txt", "r");
    for (char i; (i=fgetc(fp)!='\n');); 
    for (char i; (i=fgetc(fp)!='\n');); 
    for (char i; (i=fgetc(fp)!='\n');); 
    
    assert(leer_jugadas(fp, &juego)==TRUE);
    fclose(fp);
}

void test_jugada_valida(){
    info_tablero partida;
    info_jugada juego;
    int jugada[2], direcciones[8];

    iniciar_tablero(&partida); // Tenemos las 4 fichas inciales del juego puestas
    partida.jugadorBlanco = "Alex";
    partida.jugadorNegro = "Ignacio";
    juego.turno = 'N';

    transformar_jugada("C4", jugada);
    assert(jugada_validas(&partida,&juego, jugada, direcciones)==TRUE);
    transformar_jugada("H8", jugada);
    assert(jugada_validas(&partida,&juego ,jugada, direcciones)==FALSE);
}

void test_validar_jugada_auxiliar(){
    info_tablero partida;
    info_jugada juego;
    int jugada[2];

    iniciar_tablero(&partida);
    partida.jugadorBlanco = "Martin";
    partida.jugadorNegro = "Valentin";
    juego.turno = 'N';

    transformar_jugada("F5", jugada);
    assert(validar_jugada_auxiliar(&partida,&juego, jugada, 1, 0)==0);
    assert(validar_jugada_auxiliar(&partida,&juego, jugada, 1, -1)==0);
}

void test_jugada_en_rango(){
    int ficha[2];

    transformar_jugada("H8", ficha);
    assert(jugada_en_rango(ficha)==TRUE);

    transformar_jugada("N9", ficha);
    assert(jugada_en_rango(ficha)==FALSE);
    transformar_jugada("FF", ficha);
    assert(jugada_en_rango(ficha)==FALSE);
}

void test_movimiento_disponible(){
    info_tablero partida;
    info_jugada juego;
    iniciar_tablero(&partida);

    // Comprobamos que al inicio del juego haya movimientos disponibles
    juego.turno = 'B';
    int hay_movimientos = movimiento_disponible(&partida, &juego);
    assert(hay_movimientos == TRUE);

    juego.turno = 'N';
    hay_movimientos = movimiento_disponible(&partida, &juego);
    assert(hay_movimientos == TRUE);

    
}
