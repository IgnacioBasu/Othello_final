from src.final import jugada_en_lista

def test_jugada_en_lista():
  jugadas = [((0,0),(3,3)),((6,7),(3,3))]
  jugada = [(6,7),(0,0)]
  assert jugada == jugada_en_lista(jugadas)
 