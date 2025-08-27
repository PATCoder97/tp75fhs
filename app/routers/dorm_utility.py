from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date

from app.database.session import get_db
from app.schemas.dorm_utility import DormUtilityCreate, DormUtilityOut
from app.services.dorm_utility_service import DormUtilityService
from app.core.security import login_required

router = APIRouter(prefix="/dorm-utilities", tags=["dorm-utilities"])

@router.post("/", response_model=DormUtilityOut)
async def create_utility(
    utility: DormUtilityCreate,
    db: AsyncSession = Depends(get_db)
):
    service = DormUtilityService(db)
    return await service.create_utility(utility)

@router.post("/batch", response_model=List[DormUtilityOut])
async def create_utilities_batch(
    utilities: List[DormUtilityCreate],
    db: AsyncSession = Depends(get_db)
):
    service = DormUtilityService(db)
    return await service.create_utilities(utilities)

@router.get("/", response_model=List[DormUtilityOut], dependencies=[Depends(login_required)])
async def get_utilities(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[str] = None,
    dorm_no: Optional[str] = None,
    period_month: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    service = DormUtilityService(db)
    return await service.get_utilities(
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        dorm_no=dorm_no,
        period_month=period_month
    )

@router.get("/{utility_id}", response_model=DormUtilityOut, dependencies=[Depends(login_required)])
async def get_utility(
    utility_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = DormUtilityService(db)
    utility = await service.get_utility_by_id(utility_id)
    if not utility:
        raise HTTPException(status_code=404, detail="Utility record not found")
    return utility
