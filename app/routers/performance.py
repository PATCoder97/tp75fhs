from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database.session import get_db
from app.schemas.performance import PerformanceCreate, PerformanceOut
from app.services.performance_service import PerformanceService
from app.core.security import login_required

router = APIRouter(prefix="/performance", tags=["performance"])

@router.post("/", response_model=PerformanceOut)
async def create_performance(
    performance: PerformanceCreate,
    db: AsyncSession = Depends(get_db)
):
    service = PerformanceService(db)
    return await service.create_performance(performance)

@router.post("/batch", response_model=List[PerformanceOut])
async def create_performances_batch(
    performances: List[PerformanceCreate],
    db: AsyncSession = Depends(get_db)
):
    service = PerformanceService(db)
    return await service.create_performances(performances)

@router.get("/", response_model=List[PerformanceOut], dependencies=[Depends(login_required)])
async def get_performances(
    skip: int = 0,
    limit: int = 100,
    employee_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    service = PerformanceService(db)
    return await service.get_performances(skip, limit, employee_id)

@router.get("/{performance_id}", response_model=PerformanceOut, dependencies=[Depends(login_required)])
async def get_performance(
    performance_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = PerformanceService(db)
    result = await service.get_performance_by_id(performance_id)
    if not result:
        raise HTTPException(status_code=404, detail="Performance not found")
    return result
