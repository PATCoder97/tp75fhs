from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.performance import Performance
from app.schemas.performance import PerformanceCreate, PerformanceUpdate

class PerformanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_performance(self, performance: PerformanceCreate) -> Performance:
        db_perf = Performance(**performance.model_dump())
        self.db.add(db_perf)
        await self.db.commit()
        await self.db.refresh(db_perf)
        return db_perf

    async def create_performances(self, performances: List[PerformanceCreate]) -> List[Performance]:
        db_perfs = [Performance(**p.model_dump()) for p in performances]
        self.db.add_all(db_perfs)
        await self.db.commit()
        for perf in db_perfs:
            await self.db.refresh(perf)
        return db_perfs

    async def get_performances(
        self, 
        skip: int = 0, 
        limit: int = 100,
        employee_id: Optional[str] = None
    ) -> List[Performance]:
        query = select(Performance)
        if employee_id:
            query = query.filter(Performance.employee_id == employee_id)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_performance_by_id(self, id: int) -> Optional[Performance]:
        result = await self.db.execute(
            select(Performance).filter(Performance.id == id)
        )
        return result.scalar_one_or_none()
