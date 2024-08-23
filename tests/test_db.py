from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import User


def test_create_user(session: Session):
    user = User(
        username='willrockoliv',
        email='willrockoliv@github.com',
        password='minha_senha-legal',
    )

    session.add(user)
    session.commit()

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    assert db_user is not None
    assert db_user.username == user.username
    assert db_user.email == user.email
    assert db_user.password == user.password
