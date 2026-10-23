import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.user import Role

def test_create_user(session):
    user = User(
        username="Pietro",
        password_hash="rw123",
        email="pietro.martinet@gmail.com",
    )

    session.add(user)
    session.commit()

    assert user.id is not None
    assert user.username == "Pietro"
    assert user.password_hash == "rw123"
    assert user.email == "pietro.martinet@gmail.com"
    assert user.role == Role.NOT_SPECIFIED
    assert user.created_at is not None

def test_query_user(session):
    user = User(
        username="Pietro",
        password_hash="rw123",
        email="pietro.martinet@gmail.com",
    )

    session.add(user)
    session.commit()

    user_id = user.id

    query = session.get(User, user_id)

    assert query.id is not None
    assert query.username == "Pietro"
    assert query.password_hash == "rw123"
    assert query.email == "pietro.martinet@gmail.com"
    assert query.role == Role.NOT_SPECIFIED
    assert query.created_at is not None

def test_user_null_username(session):
    user = User(
        password_hash="rw123",
        email="pietro.martinet@gmail.com",
    )

    with pytest.raises(IntegrityError):
        session.add(user)
        session.commit()

def test_user_null_password_hash(session):
    user = User(
        username="Pietro",
        email="pietro.martinet@gmail.com",
    )

    with pytest.raises(IntegrityError):
        session.add(user)
        session.commit()

def test_user_null_email(session):
    user = User(
        username="Pietro",
        password_hash="rw123",
    )

    with pytest.raises(IntegrityError):
        session.add(user)
        session.commit()

def test_duplicate_username(session):
    user1 = User(
        username="Pietro",
        password_hash="rw123",
        email="pietro.martinet@gmail.com",
    )

    user2 = User(
        username="Pietro",
        password_hash="rw123",
        email="pietro.martinet@gmail.com",
    )

    session.add(user1)
    session.commit()

    with pytest.raises(IntegrityError):
        session.add(user2)
        session.commit()