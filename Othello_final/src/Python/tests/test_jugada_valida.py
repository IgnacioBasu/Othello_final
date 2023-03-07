from src.final import jugada_valida

def test_jugada_valida():
    assert False == jugada_valida((2,3,4))
    assert False == jugada_valida((8,8))
    assert True == jugada_valida((2,3))