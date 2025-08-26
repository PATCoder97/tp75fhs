from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from datetime import date

from app.models.dorm_utility import DormUtility
from app.schemas.dorm_utility import DormUtilityCreate, DormUtilityUpdate

class DormUtilityService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_utility(self, utility: DormUtilityCreate) -> DormUtility:
        db_utility = DormUtility(**utility.model_dump())
        self.db.add(db_utility)
        await self.db.commit()
        await self.db.refresh(db_utility)
        return db_utility

    async def create_utilities(self, utilities: List[DormUtilityCreate]) -> List[DormUtility]:
        db_utilities = [DormUtility(**u.model_dump()) for u in utilities]
        self.db.add_all(db_utilities)
        await self.db.commit()
        for utility in db_utilities:
            await self.db.refresh(utility)
        return db_utilities

    async def get_utilities(
        self,
        skip: int = 0,
        limit: int = 100,
        employee_id: Optional[str] = None,
        dorm_no: Optional[str] = None,
        period_month: Optional[date] = None
    ) -> List[DormUtility]:
        query = select(DormUtility)
        
        if employee_id:
            query = query.filter(DormUtility.employee_id == employee_id)
        if dorm_no:
            query = query.filter(DormUtility.dorm_no == dorm_no)
        if period_month:
            query = query.filter(DormUtility.period_month == period_month)
            
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_utility_by_id(self, utility_id: int) -> Optional[DormUtility]:
        result = await self.db.execute(
            select(DormUtility).filter(DormUtility.id == utility_id)
        )
        return result.scalar_one_or_none()
