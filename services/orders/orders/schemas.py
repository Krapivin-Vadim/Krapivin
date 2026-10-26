"""Описание того, что сервис принимает и что отдаёт."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrderCreate(BaseModel):
    """Данные для создания заказа."""

    account_id: int = Field(examples=[1])
    item: str = Field(min_length=1, max_length=120, examples=["Ноутбук"])
    quantity: int = Field(ge=1, examples=[1])


class OrderRead(BaseModel):
    """Карточка заказа."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    item: str
    quantity: int
    created_at: datetime


class HealthRead(BaseModel):
    """Ответ служебной проверки «жив ли сервис»."""

    status: str
    service: str