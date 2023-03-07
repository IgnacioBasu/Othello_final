from src.final import mejor_jugada

def test_mejor_jugada():
 tablero = [['X', 'X', 'X', 'N', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'N', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'B', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'B', 'X', 'X', 'X', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']]




 assert (5,2) == mejor_jugada((tablero,'B'))

