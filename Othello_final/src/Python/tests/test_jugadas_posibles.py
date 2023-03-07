from src.final import jugadas_posibles

def test_jugadas_posibles():
 tablero = [['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'N', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'N', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]


 jugadas_posible = [((2, 4), (1, 0)), ((3, 5), (0, -1)), ((4, 2), (0, 1)), ((5, 3), (-1, 0))]
 assert jugadas_posible == jugadas_posibles(tablero,'B')
 
