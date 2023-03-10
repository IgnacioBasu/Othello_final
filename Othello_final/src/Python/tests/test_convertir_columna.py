from src.final import convertir_columna

def test_convertir_columna():
  caracter = 'ABCDEFGH'
  assert 0 == convertir_columna(caracter[0])
  assert 1 == convertir_columna(caracter[1])
  assert 2 == convertir_columna(caracter[2])
  assert 3 == convertir_columna(caracter[3])
  assert 4 == convertir_columna(caracter[4])
  assert 5 == convertir_columna(caracter[5])
  assert 6 == convertir_columna(caracter[6])
  assert 7 == convertir_columna(caracter[7])

  caracteres = 'WYL5'
  assert -1 == convertir_columna(caracteres[0])
  assert -1 == convertir_columna(caracteres[1])
  assert -1 == convertir_columna(caracteres[2])
  assert -1 == convertir_columna(caracteres[3])