from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

class PerformanceBase(BaseModel):
    eval_year_month: date
    employee_id: str = Field(..., max_length=20)
    employee_name: str = Field(..., max_length=100)
    grade: str = Field(..., max_length=50)
    nationality: str = Field(..., max_length=10)
    dept_code: str = Field(..., max_length=20)
    dept_name: str = Field(..., max_length=100)
    rank_code6: str = Field(..., max_length=20)
    rank_name: str = Field(..., max_length=100)
    
    first_score: Optional[str] = Field(default=None, max_length=20)
    first_comment: Optional[str] = None
    first_supervisor: Optional[str] = Field(default=None, max_length=50)
    
    review_score: Optional[str] = Field(default=None, max_length=20)
    review_comment: Optional[str] = None
    review_supervisor: Optional[str] = Field(default=None, max_length=50)
    
    final_score: Optional[str] = Field(default=None, max_length=20)
    final_comment: Optional[str] = None
    final_supervisor: Optional[str] = Field(default=None, max_length=50)
    
    mgr_first_score: Optional[str] = Field(default=None, max_length=20)
    mgr_first_comment: Optional[str] = None
    mgr_first_supervisor: Optional[str] = Field(default=None, max_length=50)
    
    mgr_review_score: Optional[str] = Field(default=None, max_length=20)
    mgr_review_comment: Optional[str] = None
    mgr_review_supervisor: Optional[str] = Field(default=None, max_length=50)
    
    mgr_final_score: Optional[str] = Field(default=None, max_length=20)
    mgr_final_comment: Optional[str] = None
    mgr_final_supervisor: Optional[str] = Field(default=None, max_length=50)
    
    leave_days_total: Optional[float] = None

class PerformanceCreate(PerformanceBase):
    pass

class PerformanceUpdate(PerformanceBase):
    pass

class PerformanceOut(PerformanceBase):
    id: int

    class Config:
        from_attributes = True
