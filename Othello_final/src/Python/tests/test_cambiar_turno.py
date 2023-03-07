from src.final import cambiar_turno

def test_cambiar_turno():
  assert 'B' == cambiar_turno('N')
  assert 'N' == cambiar_turno('B')