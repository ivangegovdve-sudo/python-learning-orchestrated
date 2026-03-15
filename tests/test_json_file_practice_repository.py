from python_learning_orchestrated.adapters.json_file_practice_repository import _to_int

def test_to_int_with_valid_string_returns_int():
    assert _to_int("123", 42) == 123

def test_to_int_with_invalid_string_returns_default():
    assert _to_int("abc", 42) == 42

def test_to_int_with_integer_returns_integer():
    assert _to_int(123, 42) == 123

def test_to_int_with_none_returns_default():
    assert _to_int(None, 42) == 42
