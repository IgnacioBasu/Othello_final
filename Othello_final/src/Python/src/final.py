import sys # Me permite almacenar los datos pedidos en consola, en argv[]
from random import choice # Usado para la jugada aleatoria de la maquina
import os

# Tablero := List(List(Str))
# Tupla_numerica := tuple[int, int]
# Lista_de_tuplas_numericas:= List[tuple[int, int]]
# Archivo_entrada: tuple[Tablero, Str]

# imprimir_tablero: Tablero -> None
def imprimir_tablero(tablero: list[list[str]]) -> None:
  """
  Esta funcion nos permite imprimir el tablero que le pasemos.
  """
  print()
  print("    A B C D E F G H ")
  print("    - - - - - - - - ")
  for i, fila in enumerate(tablero):
    print(i + 1, end = ' | ')
    for valor in fila:
      print(valor, end = ' ')
    print('|', i + 1)
  print("    - - - - - - - - ")
  print("    A B C D E F G H ")
  print()
#------------------------------------------------------------------------------#
# convertir_columna: String -> Int
def convertir_columna(jugada: str) -> int:
  """
  Esta funcion nos pasa con el uso de un diccionario el string que representa la
  columna a un dato tipo int, esto es para poder usar la coordenada luego.
  """
  # Diccionario de columnas con su representación numérica
  letras = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
  try:
    return letras[str.upper(jugada[0])]
  except KeyError:
    return -1

# convertir_fila: String -> Int
def convertir_fila(caracter: str) -> int:
  '''
  Esta funcion nos pasa el entero que representa la fila a una escala menor, ya 
  que el programa arranca a contar de 0
  '''
  try:
    return int(caracter) - 1
  except:
    return -1 # El programa sólo verifica que el dato es erróneo luego

# traducir_jugada: Tupla_numerica -> String
def traducir_jugada(jugada: tuple[int, int]) -> str :
  '''
  Esta funcion toma una coordenada numerica y la transforma al formato de letra 
  y numero.
  '''
  letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  try:
    return str(letras[jugada[1]]) + str(int(jugada[0])+1) 
  except :
    return ""

#------------------------------------------------------------------------------#
def clear() -> None:
  '''
  Esta funcion nos permite limpiar la pantalla en ambos sistemas operativos, ya 
  sea windows o linux.
  '''
  os.system('cls' if os.name == 'nt' else 'clear')

#------------------------------------------------------------------------------#
# eliminar_duplicados: Lista_de_tuplas_numericas -> Lista_de_tuplas_numericas
def eliminar_duplicados(lista: list[tuple[int, int]]) -> list[tuple[int, int]]:
    '''
    Esta funcion nos elimina los elementos duplicados de una lista de tuplas.
    '''
    lista_sin_duplicados = list(set(lista))
    return lista_sin_duplicados

# jugada_en_lista: List(tuple[Tupla_numerica, Tupla numerica]) -> Lista_de_tuplas_numericas
def jugada_en_lista (jugadas: list[tuple[tuple[int, int], tuple[int, int]]]) \
  -> list[tuple[int, int]]:
  '''
  Esta funcion nos transforma de una lista de tuplas (que tiene dos tuplas dentro)
  a una lista de tuplas sin elementos repetidos.
  '''
  lista = []
  for x in jugadas:
    lista.append(x[0])
  return eliminar_duplicados(lista)

#------------------------------------------------------------------------------#
# ingreso_de_jugada: Tablero Turno -> None
def ingreso_de_jugada(tablero: list[list[str]],turno: str)-> None:
    '''
    Esta funcion nos permite el ingreso de la jugada del jugador la cual se va a
    pedir hasta que sea una jugada dentro del tablero. Luego de transformar dicha
    jugada valida se chequea que esa jugada este dentro de la lista de posibles 
    jugadas para el jugador.
    Por ultimo, se imprime el tablero resultante.
    '''
    continuar = True
    imprimir_tablero(tablero)
    while(continuar):
        
        jugadas = jugadas_posibles(tablero,turno)
        jugadas_disponibles = jugada_en_lista(jugadas)
        print("Las jugadas disponibles son: ")
        for x in jugadas_disponibles:
          print(traducir_jugada(x))
        print()
        jugada = input("Ingrese su jugada: ")
        transformado = (convertir_fila(jugada[1]),convertir_columna(jugada[0]))
        print(transformado)
        if jugada_valida(transformado) and (transformado in jugadas_disponibles):
          for xd in jugadas:
              tablero = modificar_tablero(tablero, transformado, turno, xd[1],1)[1]
          continuar = False
        else:
         print("La jugada es invalida, reingrese la jugada")


    clear()
    print("El tablero resultante es: ")
    imprimir_tablero(tablero)
#------------------------------------------------------------------------------#
# leer_tablero_colorjugador: String -> tuple[Tablero, String]
def leer_tablero_colorjugador(origen: str) -> tuple[list[list[str]], str]:
  '''
  Esta funcion toma el archivo de entrada(en el que se encuentra el tablero y el 
  color del jugador que debe jugar) y nos devuelve una tupla que contiene dicho 
  tablero con el color de quien juega.
  '''
  tablero: list[list[str]] = [[], [], [], [], [], [], [], []]
  char = ' '
  fila = 0
  try:
      # Cierra archivo cuando termina el bloque de codigo
      with open(origen, 'r') as archivo:  
          for linea in archivo.readlines():
              if not fila == 8:
                  for char in linea:
                      if char!='\n': tablero[fila].append(char)
                  fila+=1
              else:
                color_jugador = linea[0]
  except OSError:
      print("No se pudo abrir el archivo")  

  return (tablero, color_jugador)

#------------------------------------------------------------------------------#
# jugada_maquina: Archivo_entrada -> Tablero
def jugada_maquina(archivo_tablero: tuple[list[list[str]], str]) -> list[list[str]]:
  '''
  Esta funcion toma una tupla que contiene el Tablero y el color del jugador que 
  le toca jugar. Luego a traves de la funcion jugadas_posibles obtenemos una lista
  de tuplas que contienen las jugadas con sus correspondientes direcciones. Por 
  ultimo asignamos a una variable algun valor aleatorio de esta ultima lista 
  para poder aplicar la funcion modificar_tablero con dicha jugada.
  Terminado el proceso, imprimimos el tablero resultante.
  
  '''

  movida_random = choice(jugadas_posibles(archivo_tablero[0], cambiar_turno(archivo_tablero[1])))
  print("La jugada seleccionada por la maquina es: "+traducir_jugada(movida_random[0]))
  for x in jugadas_posibles(archivo_tablero[0],cambiar_turno(archivo_tablero[1])):
    if (x[0] == movida_random[0]):
      modificar_tablero(archivo_tablero[0],x[0], cambiar_turno(archivo_tablero[1]),x[1],1)
           
  print("El tablero despues que jugo la maquina quedo en: ")
  imprimir_tablero(archivo_tablero[0])
  return archivo_tablero[0]

#------------------------------------------------------------------------------#
# movimientos_disponibles: Tablero String -> Bool
def movimientos_disponible(tablero: list[list[str]], turno: str) -> bool:
  '''
  Esta funcion con el uso de una lista que tiene todas las direcciones posibles
  que se pueden presentar (8 direcciones) y la funcion modificar tablero, intenta 
  modificar el tablero con un color dado. Luego si es posible nos devuelve True y 
  en caso contrario False. Cabe aclarar que antes de ver si podemos modificar el 
  tablero, chequeamos que la posicion este vacia(sin fichas).
  '''
  direcciones = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
  for fila, lista in enumerate(tablero):
    for columna, ficha in enumerate(lista):
      if (tablero[fila][columna] == 'X'):   
        for direccion in direcciones:
           if(modificar_tablero(tablero, (fila,columna), turno, direccion,2)[0]):
               return True
  
  return False

#------------------------------------------------------------------------------#
 # resultado: Tablero -> None
def resultado(tablero: list[list[str]]) -> None:
  fichas_blancas = 0
  fichas_negras = 0 
  '''
  Esta funcion toma el tablero final y recorriendolo completo cuenta la cantidad
  de fichas que hay para cada color. Luego segun la cantidad que haya nos imprime
  la situacion final del juego(Gano alguien o hubo Empate).
  '''
  for fila, lista in enumerate(tablero):
    for columna, ficha in enumerate(lista):
     if (tablero[fila][columna] == 'B'):
      fichas_blancas+=1 
     if (tablero[fila][columna] == 'N'):
      fichas_negras+=1

  if fichas_blancas > fichas_negras:
    print("Gano el jugador de fichas blancas.")
    print("Las FICHAS BLANCAS son: " + str(fichas_blancas) + "Las FICHAS NEGRAS son" + str(fichas_negras))
  elif print("Gano el jugador de fichas negras."):
    print("Las FICHAS BLANCAS son: " + str(fichas_blancas) + "Las FICHAS NEGRAS son" + str(fichas_negras))
  else:
    print("Hubo un empate.") 
    print("Las FICHAS BLANCAS y FICHAS NEGRAS son " + str(fichas_blancas)) 

#------------------------------------------------------------------------------#
# jugar_Othello: Str Str Str -> None
def jugar_Othello(origen: str, color: str, nivel: str) -> None:
  '''
  Esta funcion nos permite jugar a Othello. Arranca guardando el tablero y el 
  color de quien le toca jugar en la variable archivo_tablero. Luego entra en un
  ciclo while que va a funcionar mientras que haya jugadas posibles para alguno de
  los dos jugadores. En dicho ciclo hay condicionales que revisan a quien le toca 
  jugar (jugador o maquina de nivel 0 o 1)y si es posible que 
  juegue(si hay movimientos para el jugador actual). Notese que esta contemplado
  cuando se deba pasar de turno gracias a los condicionales.
  Por ultimo, cuando ya no hay movimientos disponibles para ningun jugador, 
  la funcion resultado nos imprime la condicion final del juego.
  '''
  archivo_tablero = leer_tablero_colorjugador(origen)
  turno = ''
  #Debo hacer esto porque no se puede asignar valor de tupla a una variable
  turno = ' '.join(list(archivo_tablero[1]))  
  # turno es el que debe jugar
  # color es el que ingreso junto con el nivel de maquina
  imprimir_tablero(archivo_tablero[0])
  input("Presione enter para iniciar")
  clear()
  while(movimientos_disponible(archivo_tablero[0],'B') or movimientos_disponible(archivo_tablero[0],'N')):
    if (turno == color ):
      if(movimientos_disponible(archivo_tablero[0],color)):
        ingreso_de_jugada(archivo_tablero[0],color)
        turno = cambiar_turno(turno)
      else:
        turno = cambiar_turno(turno)
    else:
      if(movimientos_disponible(archivo_tablero[0],turno)):
        if(nivel == "0"):
          jugada_maquina(archivo_tablero)
          turno = cambiar_turno(turno)
        else:
          jugada_inteligente(archivo_tablero)
          turno = cambiar_turno(turno)
      else:
        turno = cambiar_turno(turno)

  resultado(archivo_tablero[0])     
#------------------------------------------------------------------------------#
# modificar_tablero: Tablero (Int, Int) String (Int, Int) Int -> (Bool, Tablero)
def modificar_tablero(tablero: list[list[str]], jugada: tuple,\
   turno: str, direccion: tuple,opcion:int) -> tuple[bool,list[list[str]]]:
  '''
  Toma como parámetros el tablero, la posición jugada (VÁLIDA), de quién es el
  turno y la dirección que quiere modificar (8 posibles).
  La función hace el movimiento COMPLETO en una dirección indicada, es decir,
  voltea todas las fichas correspondientes en una dirección siempre y cuando haya
  fichas que voltear.
  El parámetro 'dirección' es una tupla de dos números que pueden ser -1, 0 y 1.
  Los mismos reflejan la dirección fila/columna en la que se está desplazando
  respectivamente. La dirección (0, 0) no existe.
  '''
  # Asignaciones
  j_fila = jugada[0] # jugada_fila
  j_colum = jugada[1] # jugada_columna
  vert = direccion[0] # Vertical: variación en las filas
  horiz = direccion[1] # Horizontal: variación en las columnas

  delta_final = 0 # Representa la cantidad final de fichas a voltear
  delta = 1 # Contador momentáneo/hipotético de fichas a cambiar

  continuar = True
  while continuar:
    # Caso en el que la jugada se salga del tablero
    if (j_fila + delta * vert not in range(8) or
        j_colum + delta * horiz not in range(8)):
      continuar = False
    elif delta == 1: # Solo si es adyacente a la jugada
      # Caso que haya una ficha del mismo color o no hay ninguna ficha
      if tablero[j_fila + delta * vert][j_colum + delta * horiz] in ('X', turno):
        continuar = False
    # Caso que no haya ninguna ficha
    elif tablero[j_fila + delta * vert][j_colum + delta * horiz] == "X":
      continuar = False
    # Caso que haya una ficha del mismo color LUEGO de una o mas del otro color
    elif tablero[j_fila + delta * vert][j_colum + delta * horiz] == turno:
      delta_final = delta # Se va a modificar el tablero delta lugares
      continuar = False
    # Desplaza delta para analizar la siguiente posición
    delta += 1
  
  # Cambia el color de las fichas encerradas (delta_final lugares)
  if(opcion == 1):
    for lugar in range(1, delta_final):
         tablero[j_fila + lugar * vert][j_colum + lugar * horiz] = turno
    tablero[jugada[0]][jugada[1]] = turno

    
    
  if(delta_final >= 1):
    return (True, tablero)
  else:
    return (False,tablero) 

# contar_modificar: Tablero Tupla_numerica String Tupla_numerica Int -> Int
def contar_modificado(tablero: list[list[str]], jugada: tuple,\
   turno: str, direccion: tuple) -> int:
  '''
  Esta funcion es muy similar a modificar_tablero. La diferencia es que esta 
  funcion dado un Tablero, una jugada, el color del jugador y una 
  de las 8 direcciones posibles nos devuelve la cantidad de fichas que da vuelta 
  del jugador 
  '''
  # Asignaciones
  j_fila = jugada[0] # jugada_fila
  j_colum = jugada[1] # jugada_columna
  vert = direccion[0] # Vertical: variación en las filas
  horiz = direccion[1] # Horizontal: variación en las columnas

  delta_final = 0 # Representa la cantidad final de fichas a voltear
  delta = 1 # Contador momentáneo/hipotético de fichas a cambiar

  continuar = True
  while continuar:
    # Caso en el que la jugada se salga del tablero
    if (j_fila + delta * vert not in range(8) or
        j_colum + delta * horiz not in range(8)):
      continuar = False
    elif delta == 1: # Solo si es adyacente a la jugada
      # Caso que haya una ficha del mismo color o no hay ninguna ficha
      if tablero[j_fila + delta * vert][j_colum + delta * horiz] in ('X', turno):
        continuar = False
    # Caso que no haya ninguna ficha
    elif tablero[j_fila + delta * vert][j_colum + delta * horiz] == "X":
      continuar = False
    # Caso que haya una ficha del mismo color LUEGO de una o mas del otro color
    elif tablero[j_fila + delta * vert][j_colum + delta * horiz] == turno:
      delta_final = delta # Se va a modificar el tablero delta lugares
      continuar = False
    # Desplaza delta para analizar la siguiente posición
    delta += 1
 
    return (delta_final+1)

# mejor_jugada: Archivo_entrada -> Tupla_numerica
def mejor_jugada(archivo_tablero: tuple[list[list[str]], str]) -> tuple[int, int]:
    '''
    Esta funcion nos devuelve la posicion de la ficha que genera mas cambios al 
    jugador enemigo. A traves de un ciclo anidado en el que recorremos la lista de
    posiciones que se pueden colocar ficha (segun color de jugador) y probamos las
    8 direcciones posibles, logramos crear una lista de tuplas en la que tenemos
    la posicion de la ficha junto con el numero de cambios que genera. Por ultimo
    de esa lista extraemos y retornamos la posicion de ficha que este junto
     al mayor numero(numero de cambios que genera).
    
    '''
    movidas = 0
    lista = []
    indice_max = 0
    maximo = float('-inf')
    direcciones = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
    jugadas = jugadas_posibles(archivo_tablero[0],cambiar_turno(archivo_tablero[1]))
    jugadas_disponibles = jugada_en_lista(jugadas)
    for x in jugadas_disponibles:
      for y in direcciones:
        if modificar_tablero(archivo_tablero[0],x,cambiar_turno(archivo_tablero[1]),y,2)[0]:
          movidas+= contar_modificado(archivo_tablero[0],x,cambiar_turno(archivo_tablero[1]),y)
      lista.append((x,movidas))
    
    for i, tupla in enumerate(lista):
      if tupla[1] > maximo:
        maximo = tupla[1]
        indice_max = i

    tupla_con_maximo = lista[indice_max]
    resultado = tupla_con_maximo[0]

    return resultado
  
#-------------------------------------------------------------------------------
# jugada_inteligente : Archivo_entrada -> Tablero
def jugada_inteligente(archivo_tablero: tuple[list[list[str]], str])-> list[list[str]]:
  '''
  Esta funcion junto con la funcion mejor_jugada nos permite hacer que la 
  maquina nivel 1 haga siempre la jugada que genere mayores cambios. Con la 
  posicion de ficha que genera mayores cambios(dada por mejor_jugada) hacemos todas
  las modificaciones del tablero posibles con esa posicion de ficha. Por ultimo
  imprimimos y retornamos el tablero resultante.
  '''
  direcciones = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
  # Cuando hay dos jugadas que mueven las mismas fichas, elige una sola de manera aleatoria
  print("-------------------------------------------------------------------")
  print("La maquina juega con:  " + cambiar_turno(archivo_tablero[1]))
  mejorJugada = mejor_jugada(archivo_tablero)
  print("La mejor jugada y la elegida es:" + str(traducir_jugada(mejorJugada)))
  for x in direcciones:
    if modificar_tablero(archivo_tablero[0],mejorJugada,cambiar_turno(archivo_tablero[1]),x,2)[0]:
      modificar_tablero(archivo_tablero[0],mejorJugada,cambiar_turno(archivo_tablero[1]),x,1)

  imprimir_tablero(archivo_tablero[0])
  print("-------------------------------------------------------------------")
  input("Presione para seguir jugando")
  clear()

  return archivo_tablero[0]
#------------------------------------------------------------------------------# 
# jugadas_posibles: Tablero String -> List(tuple[Tupla_numerica, Tupla_numerica]))
def jugadas_posibles(tablero: list[list[str]], turno: str) -> \
   list[tuple[tuple[int, int], tuple[int, int]]]:
  '''
  Esta funcion con el uso de una lista que tiene todas las direcciones posibles
  que se pueden presentar (8 direcciones) y la funcion modificar tablero, intenta 
  modificar el tablero con un color dado. Luego si es posible nos devuelve, en una
  lista, las tuplas con la posicion para poner ficha y su respectiva direccion.
   Cabe aclarar que antes de ver si podemos modificar el tablero, chequeamos que
    la posicion este vacia(sin fichas).
  '''
  direcciones = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
  movimientos_validos = []
  for fila, lista in enumerate(tablero):
      for columna, ficha in enumerate(lista):
          if (tablero[fila][columna] == 'X'):   
                  for direccion in direcciones:
                      if(modificar_tablero(tablero, (fila,columna), turno, direccion,2)[0]):
                          movimientos_validos.append(((fila,columna),direccion))           
                    
        
  return movimientos_validos

#------------------------------------------------------------------------------#
# jugada_valida: Tupla_numerica -> Bool
def jugada_valida(jugada: tuple[int, int]) -> bool:
  '''
  Esta funcion nos permite ver si una jugada dada como coordena es valida,
  es decir, chequeamos que sean solo dos valores y que dichos valores esten entre
  0 y 7 (esto ya que el programa cuenta desde 0).En caso que no haya ningun error
  de formato, la funcion nos devuelve True y si no False.
  '''
  if (len(jugada) != 2):
    print("La jugada es invalida debe tener solo dos caracteres")
    return False
  if jugada[0] not in (0,1,2,3,4,5,6,7) \
    or jugada[1] not in (0,1,2,3,4,5,6,7):
    print("La jugada tiene un formato invalido")
    return False
  else:
    return True

#------------------------------------------------------------------------------#
# cambiar_turno: String -> String
def cambiar_turno(turno: str) -> str:
  '''
  Esta funcion nos permite cambiar el turno del jugador pasandole el color actual.
  '''
  return ("B" if turno == "N" else "N")

#------------------------------------------------------------------------------#
# chequeo_ingreso_color_nivel: String String -> Bool
def chequeo_ingreso_color_nivel(color: str, nivel: str) -> bool:
  """
  Chequeo que los argumentos dados esten dentro de lo pedido, ya sea  un color 
  de ficha existente o el nivel de la maquina con el que se desea jugar.
  """
  if color not in ("N", "B", "n", "b"):
    print("El segundo argumento debe ser el color (B/N/b/n)")
    return False
  elif nivel not in ("1", "0"):
    print("EL tercer argumento debe ser el nivel del juego (0/1)")
    return False
  else:
    return True

#------------------------------------------------------------------------------#
def chequeo_previo_y_juego() -> None:
  """
  Chequeo que los argumentos (archivo, color jugador, nivel de maquina) antes de
  jugar sean correctos y si se puede jugar el programa sigue, caso contrario 
  pido reingreso de los argumentos.
  """
  if len(sys.argv) == 4:
    if chequeo_ingreso_color_nivel(sys.argv[2], sys.argv[3]): #Chequeo que este bien puesto color y nivel
      jugar_Othello(sys.argv[1],sys.argv[2], sys.argv[3])  #Se chequea que el tablero este ok y se juega 
    else:
      print("Debe reingresar el nombre del archivo con la partida, el color con el que quiere jugar y el nivel del programa que desee")
  else:
    print("Cantidad de argumentos erronea. Ingrese origen, color, y nivel")

#------------------------------------------------------------------------------#
def main():
  chequeo_previo_y_juego() 

main()
  



    

   




