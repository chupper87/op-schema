import pytest
from Backend.app.core.security import get_password_hash, verify_password

def test_get_password_hash():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert hashed_password is not None
    assert hashed_password != password
    assert verify_password(password, hashed_password)

