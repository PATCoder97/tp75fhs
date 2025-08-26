# schemas/hrs.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# ---------- Employee ----------
class EmployeeResp(BaseModel):
    chinese_name: str | None = Field(default=None, max_length=100)
    vietnamese_name: str | None = Field(default=None, max_length=100)
    # service của bạn đang trả/parse theo dạng date yyyymmdd,
    # nhưng ở model cũ để datetime | None -> giữ nguyên cho tương thích
    date_of_birth: datetime | None = None
    date_of_joining: datetime | None = None
    department: str | None = Field(default=None, max_length=100)
    position: str | None = Field(default=None, max_length=100)
    date_of_appointment: datetime | None = None
    rank: str | None = Field(default=None, max_length=50)
    rank_start_date: datetime | None = None
    employee_id: str | None = Field(default=None, max_length=20)
    last_updated: datetime | None = None
    room_code: str | None = Field(default=None, max_length=20)
    effective_date: datetime | None = None
    basic_salary: float | None = None
    contract_date: datetime | None = None
    official_date: datetime | None = None
    exp_date: datetime | None = None
    current_address: str | None = Field(default=None, max_length=200)
    household_registration: str | None = Field(default=None, max_length=200)
    phone_1: str | None = Field(default=None, max_length=20)
    phone_2: str | None = Field(default=None, max_length=20)
    spouse_name: str | None = Field(default=None, max_length=100)


# ---------- Salary ----------
class SalaryResp(BaseModel):
    # Tất cả các trường lương đều float Optional (service đã parse_salary -> float)
    tien_phat_thuc_te: float | None = None
    tong_so_luong: float | None = None
    luong_co_ban: float | None = None
    thuong_nang_suat: float | None = None
    thuong_tet: float | None = None
    tro_cap_com: float | None = None
    tro_cap_di_lai: float | None = None
    thuong_chuyen_can: float | None = None
    phu_cap_truc_ban: float | None = None
    phu_cap_ngon_ngu: float | None = None
    phu_cap_dac_biet: float | None = None
    phu_cap_chuyen_nganh: float | None = None
    phu_cap_tac_nghiep: float | None = None
    phu_cap_khu_vuc: float | None = None
    phu_cap_tc_dot_xuat: float | None = None
    phu_cap_ngay_nghi: float | None = None
    phu_cap_tc_khan_cap: float | None = None
    phu_cap_chuc_vu: float | None = None
    tro_cap_phong: float | None = None
    phat_bu: float | None = None
    thuong_cong_viec: float | None = None
    phi_khac: float | None = None
    cong: float | None = None
    tien_dong_phuc: float | None = None
    tro_cap_com2: float | None = None
    tro_cap_dt: float | None = None
    tro_cap_nghi: float | None = None
    phu_cap_tc_le: float | None = None
    phu_cap_ca: float | None = None
    phu_cap_tc2: float | None = None
    phu_cap_nghi2: float | None = None
    phu_cap_tc_kc: float | None = None
    phu_cap_tc_dem: float | None = None
    bhxh: float | None = None
    bh_that_nghiep: float | None = None
    bhyt: float | None = None
    ky_tuc_xa: float | None = None
    tien_com: float | None = None
    dong_phuc: float | None = None
    cong_doan: float | None = None
    khac: float | None = None
    nghi_phep: float | None = None
    thue_thu_nhap: float | None = None


# ---------- Archivement ----------
class ArchivementResp(BaseModel):
    # service đang tách chuỗi year|score -> để str cho an toàn
    year: str | None = Field(default=None, max_length=10)
    score: str | None = Field(default=None, max_length=20)


# ---------- Quarter ----------
class QuarterResp(BaseModel):
    FirstMonth: float | None = None
    SecondMonth: float | None = None
    ThirdMonth: float | None = None
    Percentage: float | None = None
    Work: float | None = None
    Pay: float | None = None


# ---------- Year Bonus ----------
class YearBonusResp(BaseModel):
    # Các trường định danh/chuỗi
    mnv: str | None = Field(default=None, max_length=32)
    tlcb: str | None = Field(default=None, max_length=32)
    stdltbtn: str | None = Field(default=None, max_length=32)
    capbac: str | None = Field(default=None, max_length=32)
    tile: str | None = Field(default=None, max_length=32)   # nếu phần trăm nhưng API trả string thì vẫn giữ str

    # Các trường số ngày/số tiền → float
    ktsongay: float | None = None
    ktsotien: float | None = None
    xpsongay: float | None = None
    xpsotien: float | None = None
    stienthuong: float | None = None

    # Trường này thường là chuỗi phân loại
    tpnttt: str | None = Field(default=None, max_length=32)

    # Trường này lấy từ AFT (nếu có), có thể là số → float
    tpntst: float | None = None

# ---------- On Leave ----------
class OnLeaveResp(BaseModel):
    code: str | None = Field(default=None, max_length=20)
    name: str | None = Field(default=None, max_length=100)
    quantity: str | None = Field(default=None, max_length=32)

# ---------- Order Lunch ----------
class OrderLunchResp(BaseModel):
    id_emp: str | None = Field(default=None, max_length=20)
    name: str | None = Field(default=None, max_length=100)
    time: str | None = Field(default=None, max_length=32)
    node: str | None = Field(default=None, max_length=50)


__all__ = [
    "EmployeeResp",
    "SalaryResp",
    "ArchivementResp",
    "QuarterResp",
    "YearBonusResp",
    "OnLeaveResp",
    "OrderLunchResp",
]
