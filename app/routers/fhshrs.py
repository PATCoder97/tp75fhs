from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import date

from app.integrations.fhshrs_service import (
    HRClient,
    get_employee_by_empid,
    get_salary_by_empid,
    get_archivement_by_empid,
    get_quarter_by_empid,
    get_year_bonus_by_empid,
    get_on_leave_by_empid,
    get_user_lunch_by_date_place
)
from app.schemas.fhshrs import (
    EmployeeResp,
    SalaryResp,
    ArchivementResp,
    QuarterResp,
    YearBonusResp,
    OnLeaveResp,
    OrderLunchResp
)

router = APIRouter(prefix="/hr", tags=["human-resources"])

async def get_hr_client():
    client = HRClient()
    try:
        yield client
    finally:
        await client.close()

@router.get("/employees/{emp_id}", response_model=EmployeeResp)
async def get_employee(emp_id: int, client: HRClient = Depends(get_hr_client)):
    try:
        return await get_employee_by_empid(emp_id, client)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/employees/{emp_id}/salary/{year}/{month}", response_model=SalaryResp)
async def get_salary(
    emp_id: int, 
    year: int, 
    month: int, 
    client: HRClient = Depends(get_hr_client)
):
    try:
        return await get_salary_by_empid(emp_id, year, month, client)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/employees/{emp_id}/archivements", response_model=List[ArchivementResp])
async def get_archivements(emp_id: int, client: HRClient = Depends(get_hr_client)):
    try:
        return await get_archivement_by_empid(emp_id, client)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/employees/{emp_id}/quarter/{year}/{quarter}", response_model=QuarterResp)
async def get_quarter(
    emp_id: int,
    year: int,
    quarter: int,
    client: HRClient = Depends(get_hr_client)
):
    try:
        return await get_quarter_by_empid(emp_id, year, quarter, client)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/employees/{emp_id}/year-bonus/{year}", response_model=YearBonusResp)
async def get_year_bonus(
    emp_id: int,
    year: int,
    client: HRClient = Depends(get_hr_client)
):
    try:
        return await get_year_bonus_by_empid(emp_id, year, client)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/employees/{emp_id}/leaves/{year}", response_model=List[OnLeaveResp])
async def get_leaves(
    emp_id: int,
    year: int,
    client: HRClient = Depends(get_hr_client)
):
    try:
        return await get_on_leave_by_empid(emp_id, year, client)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/lunch/{date}/{place}", response_model=List[OrderLunchResp])
async def get_lunch_orders(
    date: date,
    place: str,
    client: HRClient = Depends(get_hr_client)
):
    try:
        date_str = date.strftime("%Y%m%d")
        return await get_user_lunch_by_date_place(date_str, place, client)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
