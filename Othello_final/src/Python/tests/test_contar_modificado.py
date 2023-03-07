from src.final import contar_modificado

def test_contar_modificado():
 tablero = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'N', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'N', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]

 assert 1 == contar_modificado(tablero,(2,4),'B',(1,0))