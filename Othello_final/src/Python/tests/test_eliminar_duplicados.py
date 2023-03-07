from src.final import eliminar_duplicados

def test_eliminar_duplicados():
  jugadas = [(0,0),(3,3),(6,7),(3,3),(0,0)]
  jugadas_sindoble = [(6,7), (3,3), (0,0)]
  jugadas2 = [(0,0),(3,3),(6,7),(3,3),(0,0),(2,3)]
  jugadas_sindoble2 = [(2,3),(6,7), (3,3),(0,0)]
  assert jugadas_sindoble  == eliminar_duplicados(jugadas)
  assert jugadas_sindoble2  == eliminar_duplicados(jugadas2)