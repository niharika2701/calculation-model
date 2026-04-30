from app.auth import hash_password, verify_password

def test_hash_password_returns_string():
    hashed = hash_password("mysecretpassword")
    assert isinstance(hashed, str)

def test_hash_is_not_plain_text():
    hashed = hash_password("mysecretpassword")
    assert hashed != "mysecretpassword"

def test_verify_correct_password():
    hashed = hash_password("mysecretpassword")
    assert verify_password("mysecretpassword", hashed) is True

def test_verify_wrong_password():
    hashed = hash_password("mysecretpassword")
    assert verify_password("wrongpassword", hashed) is False

def test_different_hashes_same_password():
    hash1 = hash_password("samepassword")
    hash2 = hash_password("samepassword")
    assert hash1 != hash2  # bcrypt generates unique salts