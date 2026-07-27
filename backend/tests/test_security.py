from datetime import timedelta
from uuid import uuid4

from app.core.security import create_token, decode_access_token, hash_password, verify_password


def test_password_hash_round_trip() -> None:
    encoded = hash_password("A-secure-pilgrimage-password")
    assert encoded != "A-secure-pilgrimage-password"
    assert verify_password("A-secure-pilgrimage-password", encoded)
    assert not verify_password("wrong-password", encoded)


def test_access_token_round_trip() -> None:
    user_id = uuid4()
    assert decode_access_token(create_token(user_id, "access", timedelta(minutes=5))) == user_id
