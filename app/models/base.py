from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer


class DonatForProjectBaseCreate:
    """Base model in db from donation and project model."""

    full_amount = Column(
        Integer,
        CheckConstraint("full_amount > 0", name="check_full_amount_positive"),
        nullable=False,
        comment="Требуемая сумма, целочисленное поле; больше 0;",
    )
    invested_amount = Column(
        Integer,
        CheckConstraint(
            "invested_amount >= 0", name="check_invested_amount_positive"
        ),
        nullable=True,
        default=0,
        comment=(
            "Внесённая сумма, целочисленное поле; значение по умолчанию — 0;"
        ),
    )
    fully_invested = Column(
        Boolean,
        nullable=True,
        default=False,
        comment=(
            "Булево значение, указывающее на то, собрана ли нужная"
            " сумма (закрыт ли проект); значение по умолчанию — False;"
        ),
    )
    create_date = Column(
        DateTime,
        nullable=True,
        default=datetime.utcnow,
        comment=(
            "дата пожертвования; тип DateTime; добавляется автоматически в"
            " момент поступления пожертвования;"
        ),
    )
    close_date = Column(
        DateTime,
        nullable=True,
        comment=(
            "дата, когда вся сумма пожертвований была распределена по проектам"
            "; тип DateTime; добавляется автоматически в момент выполнения"
            " условия."
        ),
    )
