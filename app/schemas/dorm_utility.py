from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class DormUtilityBase(BaseModel):
    period_month: date
    dorm_no: Optional[str] = Field(default=None, max_length=20)
    employee_id: Optional[str] = Field(default=None, max_length=20)
    employee_name: Optional[str] = Field(default=None, max_length=100)
    
    elec_prev_read: Optional[int] = None
    elec_curr_read: Optional[int] = None
    elec_usage: Optional[int] = None
    elec_amount: Optional[int] = None
    
    water_prev_read: Optional[int] = None
    water_curr_read: Optional[int] = None
    water_usage: Optional[int] = None
    water_amount: Optional[int] = None
    
    shared_fee: Optional[int] = None
    cleaning_fee: Optional[int] = None
    total_amount: Optional[int] = None

    # @validator('elec_usage', pre=True, always=True)
    # def calculate_elec_usage(cls, v, values):
    #     if v is None and 'elec_curr_read' in values and 'elec_prev_read' in values:
    #         curr = values.get('elec_curr_read')
    #         prev = values.get('elec_prev_read')
    #         if curr is not None and prev is not None:
    #             return curr - prev
    #     return v

    # @validator('water_usage', pre=True, always=True)
    # def calculate_water_usage(cls, v, values):
    #     if v is None and 'water_curr_read' in values and 'water_prev_read' in values:
    #         curr = values.get('water_curr_read')
    #         prev = values.get('water_prev_read')
    #         if curr is not None and prev is not None:
    #             return curr - prev
    #     return v

    # @validator('total_amount', pre=True, always=True)
    # def calculate_total(cls, v, values):
    #     if v is None:
    #         total = 0
    #         for field in ['elec_amount', 'water_amount', 'shared_fee', 'cleaning_fee']:
    #             if field in values and values[field] is not None:
    #                 total += values[field]
    #         return total if total > 0 else None
    #     return v

class DormUtilityCreate(DormUtilityBase):
    pass

class DormUtilityUpdate(DormUtilityBase):
    pass

class DormUtilityOut(DormUtilityBase):
    id: int

    class Config:
        from_attributes = True
