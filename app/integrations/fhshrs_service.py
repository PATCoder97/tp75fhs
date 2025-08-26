# app/services/hr_service.py
from __future__ import annotations

import asyncio
import logging
from typing import List, Optional

from datetime import datetime, date
import httpx

from app.schemas.fhshrs import *

logger = logging.getLogger(__name__)

BASE_URL = "https://www.fhs.com.tw/ads/api/Furnace/rest/json/hr"

# ===== Utilities =====

def _first_block(text: str) -> str:
    """Lấy block đầu trước 'o|o'."""
    return (text or "").strip().split("o|o")[0].strip()

def _split_blocks(text: str) -> List[str]:
    """Tách danh sách block theo 'o|o' (loại rỗng)."""
    return [b.strip() for b in (text or "").strip().split("o|o") if b.strip()]

def parse_date(raw: str) -> Optional[date]:
    try:
        raw = (raw or "").strip()
        if len(raw) == 8:
            return datetime.strptime(raw, "%Y%m%d").date()
    except Exception:
        pass
    return None

def parse_salary(raw: str) -> Optional[float]:
    """Trả 0 nếu rỗng, -1 nếu format lỗi (giữ logic cũ)."""
    try:
        s = (raw or "").strip()
        return float(s.replace(",", "")) if s else 0
    except Exception:
        return -1

# ===== HTTP Core =====

class HRClient:
    """Client async cho HR API. Dùng 1 instance / request hoặc inject vào service."""

    def __init__(self, base_url: str = BASE_URL, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
            headers={"User-Agent": "HRClient/1.0"},
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def fetch_text(self, path: str) -> str:
        url = "/" + path.lstrip("/")
        resp = await self._client.get(url)
        resp.encoding = "utf-8"
        if resp.status_code != httpx.codes.OK:
            raise ValueError(f"HTTP {resp.status_code} khi gọi {self.base_url}{url}")
        text = (resp.text or "").strip()
        if not text:
            raise ValueError(f"Dữ liệu rỗng từ {self.base_url}{url}")
        return text


# ===== Service Functions (async) =====

async def get_employee_by_empid(empid: int, client: HRClient) -> EmployeeResp:
    text = await client.fetch_text(f"s10/VNW00{empid:05d}")
    fields = _first_block(text).split("|")
    if len(fields) < 22:
        raise ValueError("Dữ liệu trả về không đầy đủ cho employee")

    return EmployeeResp(
        chinese_name=fields[0],
        vietnamese_name=fields[1],
        date_of_birth=parse_date(fields[2]),
        date_of_joining=parse_date(fields[3]),
        department=fields[4],
        position=fields[5],
        date_of_appointment=parse_date(fields[6]),
        rank=fields[7],
        rank_start_date=parse_date(fields[8]),
        employee_id=fields[9],
        last_updated=parse_date(fields[10]),
        room_code=fields[11],
        effective_date=parse_date(fields[12]),
        basic_salary=parse_salary(fields[13]),
        contract_date=parse_date(fields[14]),
        official_date=parse_date(fields[15]),
        exp_date=parse_date(fields[16]),
        current_address=fields[17],
        household_registration=fields[18],
        phone_1=fields[19],
        phone_2=fields[20],
        spouse_name=fields[21],
    )


async def get_salary_by_empid(empid: int, year: int, month: int, client: HRClient) -> SalaryResp:
    text = await client.fetch_text(f"s16/VNW00{empid:05d}vkokv{year}-{month:02d}")
    fields = _first_block(text).split("|")
    if len(fields) < 45:
        raise ValueError("Dữ liệu lương không đầy đủ")

    return SalaryResp(
        tien_phat_thuc_te=parse_salary(fields[43]),
        tong_so_luong=parse_salary(fields[32]),
        luong_co_ban=parse_salary(fields[44]),
        thuong_nang_suat=parse_salary(fields[2]),
        thuong_tet=parse_salary(fields[3]),
        tro_cap_com=parse_salary(fields[4]),
        tro_cap_di_lai=parse_salary(fields[5]),
        thuong_chuyen_can=parse_salary(fields[6]),
        phu_cap_truc_ban=parse_salary(fields[7]),
        phu_cap_ngon_ngu=parse_salary(fields[8]),
        phu_cap_dac_biet=parse_salary(fields[9]),
        phu_cap_chuyen_nganh=parse_salary(fields[10]),
        phu_cap_tac_nghiep=parse_salary(fields[11]),
        phu_cap_khu_vuc=parse_salary(fields[12]),
        phu_cap_tc_dot_xuat=parse_salary(fields[13]),
        phu_cap_ngay_nghi=parse_salary(fields[14]),
        phu_cap_tc_khan_cap=parse_salary(fields[15]),
        phu_cap_chuc_vu=parse_salary(fields[16]),
        tro_cap_phong=parse_salary(fields[17]),
        phat_bu=parse_salary(fields[18]),
        thuong_cong_viec=parse_salary(fields[19]),
        phi_khac=parse_salary(fields[20]),
        cong=parse_salary(fields[21]),
        tien_dong_phuc=parse_salary(fields[22]),
        tro_cap_com2=parse_salary(fields[23]),
        tro_cap_dt=parse_salary(fields[24]),
        tro_cap_nghi=parse_salary(fields[25]),
        phu_cap_tc_le=parse_salary(fields[26]),
        phu_cap_ca=parse_salary(fields[27]),
        phu_cap_tc2=parse_salary(fields[28]),
        phu_cap_nghi2=parse_salary(fields[29]),
        phu_cap_tc_kc=parse_salary(fields[30]),
        phu_cap_tc_dem=parse_salary(fields[31]),
        bhxh=parse_salary(fields[33]),
        bh_that_nghiep=parse_salary(fields[34]),
        bhyt=parse_salary(fields[35]),
        ky_tuc_xa=parse_salary(fields[36]),
        tien_com=parse_salary(fields[37]),
        dong_phuc=parse_salary(fields[38]),
        cong_doan=parse_salary(fields[39]),
        khac=parse_salary(fields[40]),
        nghi_phep=parse_salary(fields[41]),
        thue_thu_nhap=parse_salary(fields[42]),
    )


async def get_archivement_by_empid(empid: int, client: HRClient) -> List[ArchivementResp]:
    text = await client.fetch_text(f"s11/VNW00{empid:05d}")
    blocks = _split_blocks(text)
    results: List[ArchivementResp] = []
    for b in blocks:
        parts = b.split("|")
        if len(parts) >= 2:
            results.append(ArchivementResp(year=parts[0], score=parts[1]))
        else:
            logger.debug("Bỏ qua block archivement không hợp lệ: %r", b)
    return results


async def get_quarter_by_empid(empid: int, year: int, quarter: int, client: HRClient) -> QuarterResp:
    text = await client.fetch_text(f"s24/VNW00{empid:05d}vkokv{year}vkokvqr{quarter}")
    fields = (text or "").strip().split("|")
    # Dùng tới index 13 → cần >= 14
    if len(fields) < 14:
        raise ValueError("Dữ liệu quý không đầy đủ")
    return QuarterResp(
        FirstMonth=parse_salary(fields[0]),
        SecondMonth=parse_salary(fields[1]),
        ThirdMonth=parse_salary(fields[2]),
        Percentage=parse_salary(fields[3]),
        Work=parse_salary(fields[12]),
        Pay=parse_salary(fields[13]),
    )


async def get_year_bonus_by_empid(empid: int, year: int, client: HRClient) -> YearBonusResp:
    empid_str = f"{empid:05d}"

    # Có thể gọi song song 2 endpoint nếu muốn
    url_bef = f"s19/VNW00{empid_str}vkokvbefvkokv{year}"
    url_aft = f"s19/VNW00{empid_str}vkokvaftvkokv{year}"

    bef_text, aft_text = await asyncio.gather(
        client.fetch_text(url_bef),
        client.fetch_text(url_aft),
    )

    bef_parts = _first_block(bef_text).split("|")
    if len(bef_parts) < 11:
        raise ValueError("Thiếu dữ liệu BEF cho thưởng năm")

    result = YearBonusResp(
        mnv=bef_parts[0],
        tlcb=bef_parts[1],
        stdltbtn=bef_parts[2],
        capbac=bef_parts[3],
        tile=bef_parts[4],
        ktsongay=bef_parts[5],
        ktsotien=bef_parts[6],
        xpsongay=bef_parts[7],
        xpsotien=bef_parts[8],
        stienthuong=bef_parts[9],
        tpnttt=bef_parts[10],
    )

    aft_parts = _first_block(aft_text).split("|")
    if aft_parts:
        # Theo code cũ: lấy phần tử cuối cho tpntst (nếu schema có)
        result.tpntst = aft_parts[-1]

    return result


async def get_on_leave_by_empid(empid: int, year: int, client: HRClient) -> List[OnLeaveResp]:
    text = await client.fetch_text(f"s02/VNW00{empid:05d}vkokv{year}vkokvb")
    blocks = _split_blocks(text)
    results: List[OnLeaveResp] = []
    for b in blocks:
        parts = b.split("|")
        if len(parts) >= 3:
            results.append(OnLeaveResp(code=parts[0], name=parts[1], quantity=parts[2]))
        else:
            logger.debug("Bỏ qua block on_leave không hợp lệ: %r", b)
    return results


async def get_user_lunch_by_date_place(date_str: str, place: str, client: HRClient) -> List[OrderLunchResp]:
    """
    date_str: 'YYYYMMDD'
    place: ví dụ 'TW' (sẽ upper)
    """
    text = await client.fetch_text(f"s27/{date_str}vkv{place.upper()}vkvVN")
    blocks = _split_blocks(text)
    results: List[OrderLunchResp] = []
    for b in blocks:
        parts = b.split("|")
        # Giả định layout: [stt?, id_emp, name, time, node, ...]
        if len(parts) >= 5:
            results.append(
                OrderLunchResp(
                    id_emp=parts[1],
                    name=parts[2],
                    time=parts[3],
                    node=parts[4],
                )
            )
        else:
            logger.debug("Bỏ qua block order lunch không hợp lệ: %r", b)
    return results
