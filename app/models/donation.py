from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.db import Base
from app.models.base import DonatForProjectBaseCreate


class Donation(DonatForProjectBaseCreate, Base):
    """Model for donations in supported project."""
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='donation_id_user'),
        comment=(
            'id пользователя, сделавшего пожертвование. Foreign Key на поле'
            ' user.id из таблицы пользователей;'
        )
    )
    comment = Column(
        String,
        nullable=True,
        comment='Комментарий, необязательное текстовое поле;'
    )

    def __repr__(self) -> str:
        return (
            f'Пожертвование от пользователя {self.user_id}'
            f' на сумму {self.full_amount}'
        )
