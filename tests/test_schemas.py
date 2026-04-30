import pytest
from pydantic import ValidationError
from app.schemas import UserCreate, UserRead
from datetime import datetime

def test_user_create_valid():
    user = UserCreate(
        username="alice",
        email="alice@example.com",
        password="securepass123"
    )
    assert user.username == "alice"
    assert user.email == "alice@example.com"

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            username="alice",
            email="not-an-email",
            password="securepass123"
        )

def test_user_create_missing_fields():
    with pytest.raises(ValidationError):
        UserCreate(username="alice")

def test_user_read_config():
    user = UserRead(
        id=1,
        username="alice",
        email="alice@example.com",
        created_at=datetime.now()
    )
    assert user.id == 1
    assert user.username == "alice"