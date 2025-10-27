import os

from fastapi import APIRouter, Depends, Query, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db

from db.CRUD import get_info_about_project

about_project_router = APIRouter()


@about_project_router.get('/')
async def get_information_about_project():
    '''о проекте'''
    response = await get_info_about_project()

    if not response:
        raise HTTPException(status_code=404, detail="Data not found")

    return response

