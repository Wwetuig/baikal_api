from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.CRUD import get_external_resources, get_external_resource_by_id

from db.database import get_db

external_resources_router = APIRouter()

@external_resources_router.get('/get_resources')
async def get_all_external_resources(db: AsyncSession = Depends(get_db)):
    data = await get_external_resources(db)
    if data is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return data

@external_resources_router.get('/get_resources/{resource_id}')
async def get_resource_by_id(
    resource_id: int,
    db: AsyncSession = Depends(get_db)
):
    data = await get_external_resource_by_id(resource_id, db)
    if data is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return data

