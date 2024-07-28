# app/schemas/reservation.py
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectSchemaBase(BaseModel):
    """Base schema for CharityProject model."""

    name: str = Field(
        min_length=1,
        max_length=100,
        title="Name charity project",
        description=(
            "Уникальноеназвание проекта, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 100 символов включительно;"
        ),
    )
    description: str = Field(
        min_length=1,
        title="Description for the charity project",
        description=(
            "Описание, обязательное поле, текст; не менее одного символа;"
        ),
    )
    full_amount: PositiveInt = Field(
        title="Full amount for supporn in charity project",
        description="Требуемая сумма, целочисленное поле; больше 0;",
    )


class CharityProjectSchemaCreate(CharityProjectSchemaBase):
    """Create schema for CharityProject model."""


class CharityProjectSchemaUpdate(CharityProjectSchemaBase):
    """Update schema for CharityProject model."""

    name: Optional[str] = Field(
        min_length=1,
        max_length=100,
        title="Name charity project",
        description=(
            "Уникальное название проекта, обязательное строковое поле;"
            " допустимая длина строки — от 1 до 100 символов включительно;"
        ),
    )
    description: Optional[str] = Field(
        min_length=1,
        title="Description for the charity project",
        description=(
            "Описание, обязательное поле, текст; не менее одного символа;"
        ),
    )
    full_amount: Optional[PositiveInt] = Field(
        title="Full amount for supporn in charity project",
        description="Требуемая сумма, целочисленное поле; больше 0;",
    )

    class Config:
        extra = Extra.forbid


class CharityProjectSchemaDB(CharityProjectSchemaBase):
    """Presentate schema for CharityProject model."""

    id: int = Field(
        title="Id project in db", description="Id проекта в базе данных"
    )
    invested_amount: int = Field(
        title="Invested amount for the charity project",
        description=(
            "Внесённая сумма, целочисленное поле; значение по умолчанию — 0;"
        ),
    )
    fully_invested: bool = Field(
        False,
        title="Are investments open to support the charity project",
        description=(
            "Булево значение, указывающее на то, собрана ли нужная"
            " сумма для проекта (закрыт ли проект); значение по умолчанию"
            " — False;"
        ),
    )
    create_date: datetime = Field(
        title="Create date for the charity project",
        description=(
            "Дата создания проекта, тип DateTime, должно добавляться"
            " автоматически в момент создания проекта."
        ),
    )
    close_date: datetime = Field(
        None,
        title="Close investments for the charity project",
        description=(
            "Дата закрытия проекта, DateTime, проставляется автоматически в"
            " момент набора нужной суммы."
        ),
    )

    class Config:
        orm_mode: bool = True
