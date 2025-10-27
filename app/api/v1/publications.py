import os

from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db

from db.CRUD import get_publications, get_publication

publications_router = APIRouter()


@publications_router.get('/')
async def get_all_publications(db: AsyncSession = Depends(get_db)):
    '''получение всех публикаций'''
    response = await get_publications(db)

    if not response:
        raise HTTPException(status_code=404, detail="Publications not found")

    return response


@publications_router.get('/{publication_id}')
async def get_publication_by_id(publication_id: int, db: AsyncSession = Depends(get_db)):
    '''получение конкретной публикации по ID'''
    response = await get_publication(publication_id, db)

    if not response:
        raise HTTPException(status_code=404, detail="Publication not found")

    return response