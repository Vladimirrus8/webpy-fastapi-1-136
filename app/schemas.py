# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CreateAdvertisementRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок объявления")
    description: str = Field(..., min_length=1, max_length=1000, description="Описание объявления")
    price: float = Field(..., gt=0, description="Цена (должна быть больше 0)")
    author: str = Field(..., min_length=1, max_length=100, description="Автор объявления")

class CreateAdvertisementResponse(BaseModel):
    id: int

class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: Optional[str] = None

class UpdateAdvertisementRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    author: Optional[str] = Field(None, min_length=1, max_length=100)

class UpdateAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: Optional[str] = None

class OKResponse(BaseModel):
    status: str = "ok"