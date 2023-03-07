from src.final import modificar_tablero

def test_modificar_tablero():
 tablero = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'N', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'N', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

 tablero1 = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'N', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]


 assert (True,tablero1) == modificar_tablero(tablero,(2,4),'B',(1,0),1)