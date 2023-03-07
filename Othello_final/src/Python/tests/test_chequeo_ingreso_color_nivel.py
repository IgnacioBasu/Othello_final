from src.final import chequeo_ingreso_color_nivel

def test_chequeo_ingreso_color_nivel():
    color = 'B'
    color1 = 'j'
    nivel = '1'

    assert False == chequeo_ingreso_color_nivel(color1, nivel)
    assert True == chequeo_ingreso_color_nivel(color,nivel)