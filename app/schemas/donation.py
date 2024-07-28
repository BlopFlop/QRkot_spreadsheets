from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationSchemmaBase(BaseModel):
    """Base schema for Donation model."""

    comment: Optional[str] = Field(
        None,
        title="Comment for donation",
        description="Комментарий, необязательное текстовое поле;",
    )
    full_amount: PositiveInt = Field(
        title="Full amount donation",
        description="сумма пожертвования, целочисленное поле; больше 0;",
    )


class DonationSchemmaCreate(DonationSchemmaBase):
    """Create schema for Donation model."""


class AllDonationsSchemaDB(DonationSchemmaBase):
    """Presentate schema for Donation model."""

    id: int = Field(
        title="Id donat in db",
        description="Id пожертвования в базе данных",
    )
    user_id: int = Field(
        title="User id make donation",
        description=(
            "Id пользователя, сделавшего пожертвование. Foreign Key на поле"
            " user.id из таблицы пользователей;"
        ),
    )
    invested_amount: int = Field(
        title="Invested amount",
        description=(
            "сумма из пожертвования, которая распределена по проектам;"
            " значение по умолчанию равно 0;"
        ),
    )
    fully_invested: bool = Field(
        False,
        title="Fully invested",
        description=(
            "булево значение, указывающее на то, все ли деньги из"
            " пожертвования были переведены в тот или иной проект; по"
            " умолчанию равно False;"
        ),
    )
    create_date: datetime = Field(
        title="Create donation",
        description=(
            "дата пожертвования; тип DateTime; добавляется автоматически в"
            " момент поступления пожертвования;"
        ),
    )
    close_date: datetime = Field(
        None,
        title="Distribution donate in all project",
        description=(
            "дата, когда вся сумма пожертвования была распределена по проектам"
            "; тип DateTime; добавляется автоматически в момент выполнения"
            " условия."
        ),
    )

    class Config:
        orm_mode: bool = True


class DonationSchemmaDB(DonationSchemmaCreate):
    """Presentate schema for Donation model."""

    id: int = Field(
        title="Id donat in db",
        description="Id пожертвования в базе данных",
    )
    create_date: datetime = Field(
        title="Create donation",
        description=(
            "дата пожертвования; тип DateTime; добавляется автоматически в"
            " момент поступления пожертвования;"
        ),
    )

    class Config:
        orm_mode: bool = True
