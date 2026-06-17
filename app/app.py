# app/app.py
from typing import Annotated, Optional
from fastapi import FastAPI, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from dependencies import get_db_session
from lifespan import lifespan
from services import (
    add_advertisement,
    get_advertisement,
    update_advertisement,
    delete_advertisement,
    search_advertisements
)

app = FastAPI(
    title="Advertisement Service",
    description="Сервис объявлений купли/продажи",
    version="1.0.0",
    lifespan=lifespan
)

# Создаём тип для зависимости сессии
SessionDep = Annotated[AsyncSession, Depends(get_db_session)]


@app.post("/advertisement", response_model=schemas.CreateAdvertisementResponse, summary="Создать новое объявление",
          status_code=201)
async def create_advertisement(
        ad_data: schemas.CreateAdvertisementRequest,
        session: SessionDep
):
    """Создание нового объявления купли/продажи"""
    new_ad = await add_advertisement(session, models.Advertisement, ad_data)
    return schemas.CreateAdvertisementResponse(id=new_ad.id)


@app.get("/advertisement/{advertisement_id}", response_model=schemas.GetAdvertisementResponse,
         summary="Получить объявление по ID")
async def get_advertisement_by_id(
        advertisement_id: int,
        session: SessionDep
):
    """Получение объявления по его ID"""
    ad = await get_advertisement(session, models.Advertisement, advertisement_id)
    return schemas.GetAdvertisementResponse(**ad.to_dict())


@app.patch("/advertisement/{advertisement_id}", response_model=schemas.UpdateAdvertisementResponse,
           summary="Обновить объявление")
async def update_advertisement_by_id(
        advertisement_id: int,
        update_data: schemas.UpdateAdvertisementRequest,
        session: SessionDep
):
    """Обновление существующего объявления"""
    updated_ad = await update_advertisement(session, models.Advertisement, advertisement_id, update_data)
    return schemas.UpdateAdvertisementResponse(**updated_ad.to_dict())


@app.delete("/advertisement/{advertisement_id}", response_model=schemas.OKResponse, summary="Удалить объявление")
async def delete_advertisement_by_id(
        advertisement_id: int,
        session: SessionDep
):
    """Удаление объявления по ID"""
    await delete_advertisement(session, models.Advertisement, advertisement_id)
    return schemas.OKResponse()


@app.get("/advertisement", response_model=list[schemas.GetAdvertisementResponse], summary="Поиск объявлений по полям")
async def search_advertisements_by_fields(
        title: Optional[str] = Query(None, description="Поиск по заголовку (частичное совпадение)"),
        description: Optional[str] = Query(None, description="Поиск по описанию (частичное совпадение)"),
        price_min: Optional[float] = Query(None, description="Минимальная цена", gt=0),
        price_max: Optional[float] = Query(None, description="Максимальная цена", gt=0),
        author: Optional[str] = Query(None, description="Поиск по автору (частичное совпадение)"),
        session: SessionDep
):
    """
    Поиск объявлений по различным полям.
    Поддерживается поиск по:
    - заголовку (частичное совпадение)
    - описанию (частичное совпадение)
    - автору (частичное совпадение)
    - диапазону цены
    """
    filters = {}
    if title:
        filters["title"] = title
    if description:
        filters["description"] = description
    if price_min is not None:
        filters["price_min"] = price_min
    if price_max is not None:
        filters["price_max"] = price_max
    if author:
        filters["author"] = author

    ads = await search_advertisements(session, models.Advertisement, filters)
    return [schemas.GetAdvertisementResponse(**ad.to_dict()) for ad in ads]