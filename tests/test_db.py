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

    session.scalar(select(User).where(User.email == 'willrockoliv@github.com'))

    assert user.username == 'willrockoliv'
