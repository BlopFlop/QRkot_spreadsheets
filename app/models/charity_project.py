from sqlalchemy import CheckConstraint, Column, String

from app.core.db import Base
from app.models.base import DonatForProjectBaseCreate


class CharityProject(DonatForProjectBaseCreate, Base):
    """Project model in need of investment."""

    name = Column(
        String(100),
        CheckConstraint("LENGTH(name) <= 100", name="check_len_name"),
        unique=True,
        nullable=False,
        comment=(
            "Уникальное название проекта, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 100 символов включительно;"
        ),
    )
    description = Column(
        String,
        nullable=False,
        comment=(
            "Описание, обязательное поле, текст; не менее одного символа;"
        ),
    )

    def __repr__(self):
        MAX_LEN_REPR_NAME = 10

        result_name: str = self.name
        if len(result_name) > MAX_LEN_REPR_NAME:
            result_name: str = f"{result_name[:MAX_LEN_REPR_NAME]}..."

        return f"Благотворительный проект {result_name}"
