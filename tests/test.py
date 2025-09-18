def test_always_pass():
    """Простой тест, чтобы проверить, что pytest работает."""
    assert True

def test_secret_number_is_4_digits():
    """Проверяем, что загаданное число — 4-значное."""
    from main import generate_number
    num = generate_number()
    assert len(num) == 4
    assert num.isdigit()