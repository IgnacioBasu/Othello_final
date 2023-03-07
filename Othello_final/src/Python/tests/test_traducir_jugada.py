from src.final import traducir_jugada

def test_traducir_jugada():
  jugadas =[(0,0),(3,3),(6,7)]
  assert 'A1' == traducir_jugada(jugadas[0])
  assert 'D4' == traducir_jugada(jugadas[1])
  assert 'H7' == traducir_jugada(jugadas[2])
