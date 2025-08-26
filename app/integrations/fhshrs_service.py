import requests
from schemas.employee import EmployeeResp
from schemas.salary import SalaryResp
from schemas.archivement import ArchivementResp
from schemas.quater import QuarterResp
from schemas.yearbonus import YearBonusResp
from schemas.onleave import OnLeaveResp
from schemas.orderlunch import OrderLunchResp
from typing import Optional, List
from datetime import datetime, date

base_url = "https://www.fhs.com.tw/ads/api/Furnace/rest/json/hr"


def parse_date(raw: str) -> Optional[date]:
    try:
        if len(raw) == 8:
            return datetime.strptime(raw, "%Y%m%d").date()
    except:
        pass
    return None


def parse_salary(s: str) -> Optional[float]:
    try:
        return float(s.replace(",", "")) if s else 0
    except:
        return -1


def get_employee_by_keyword(empid: int) -> EmployeeResp:
    url = f"{base_url}/s10/VNW00{empid:05d}"
    response = requests.get(url)
    response.encoding = "utf-8"
    raw_text = response.text

    print(raw_text.split("o|o")[0])

    fields = raw_text.strip().split("o|o")[0].split("|")
    if len(fields) < 22:
        raise ValueError("Dữ liệu trả về không đầy đủ")

    employee = EmployeeResp(
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

    return employee


def get_salary_by_empid(empid: int, year: int, month: int) -> SalaryResp:
    url = f"{base_url}/s16/VNW00{empid:05d}vkokv{year}-{month:02d}"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code != 200 or not response.text:
        raise ValueError("Không lấy được dữ liệu từ API")

    # Tách dữ liệu
    resp = response.text.strip()
    fields = resp.split("o|o")[0].split("|")

    print(resp.split("o|o")[0])

    # Kiểm tra đủ số lượng field
    if len(fields) < 45:
        raise ValueError("Dữ liệu không đầy đủ")

    # Chuẩn bị dữ liệu phẳng
    result = SalaryResp(
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

    return result


def get_archivement_by_empid(empid: int) -> List[ArchivementResp]:
    url = f"{base_url}/s11/VNW00{empid:05d}"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code != 200 or not response.text:
        raise ValueError("Không lấy được dữ liệu từ API")

    resp = response.text.strip()
    fields = [f for f in resp.split("o|o") if f.strip()]

    print(resp)

    results = []

    for field in fields:
        if "|" in field:
            year, score = field.split("|")
            results.append(ArchivementResp(year=year, score=score))

    return results


def get_quater_by_empid(empid: int, year: int, quater: int) -> QuarterResp:
    url = f"{base_url}/s24/VNW00{empid:05d}vkokv{year}vkokvqr{quater}"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code != 200 or not response.text:
        raise ValueError("Không lấy được dữ liệu từ API")

    resp = response.text.strip()

    print(resp)

    fields = resp.split("|")

    if len(fields) < 13:
        raise ValueError("Dữ liệu không đầy đủ")

    return QuarterResp(
        FirstMonth=parse_salary(fields[0]),
        SecondMonth=parse_salary(fields[1]),
        ThirdMonth=parse_salary(fields[2]),
        Percentage=parse_salary(fields[3]),
        Work=parse_salary(fields[12]),
        Pay=parse_salary(fields[13]),
    )


def get_year_bonus_by_empid(empid: int, year: int) -> YearBonusResp:
    empid_str = f"{empid:05d}"  # giống {input.EmpId:D5} trong C#

    url_bef = f"{base_url}/s19/VNW00{empid_str}vkokvbefvkokv{year}"
    url_aft = f"{base_url}/s19/VNW00{empid_str}vkokvaftvkokv{year}"

    # Lấy dữ liệu BEF
    response_bef = requests.get(url_bef)
    response_bef.encoding = "utf-8"
    if response_bef.status_code != 200 or not response_bef.text:
        raise ValueError("Không lấy được dữ liệu BEF")

    print(response_bef.text)

    parts = response_bef.text.strip().split("o|o")[0].split("|")
    if len(parts) < 11:
        raise ValueError("Thiếu dữ liệu BEF")

    result = YearBonusResp(
        mnv=parts[0],
        tlcb=parts[1],
        stdltbtn=parts[2],
        capbac=parts[3],
        tile=parts[4],
        ktsongay=parts[5],
        ktsotien=parts[6],
        xpsongay=parts[7],
        xpsotien=parts[8],
        stienthuong=parts[9],
        tpnttt=parts[10],
    )

    # Lấy dữ liệu AFT
    response_aft = requests.get(url_aft)

    print(response_aft.text)

    response_aft.encoding = "utf-8"
    if response_aft.status_code == 200 and response_aft.text.strip():
        aft_parts = response_aft.text.strip().split("o|o")[0].split("|")
        if aft_parts:
            result.tpntst = aft_parts[-1]

    return result


def get_on_leave_by_empid(empid: int, year: int) -> List[OnLeaveResp]:
    url = f"{base_url}/s02/VNW00{empid:05d}vkokv{year}vkokvb"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code != 200 or not response.text.strip():
        raise ValueError("Không lấy được dữ liệu hoặc dữ liệu rỗng")

    resp = response.text.strip()
    fields = [f for f in resp.split("o|o") if f.strip()]

    print(resp)

    results = []

    for field in fields:
        if "|" in field:
            code, name, quantity = field.split("|")
            results.append(OnLeaveResp(code=code, name=name, quantity=quantity))

    return results


def get_user_lunch_by_date_place(date: str, place: str) -> List[OrderLunchResp]:
    url = f"{base_url}/s27/{date}vkv{place.upper()}vkvVN"
    response = requests.get(url)
    response.encoding = "utf-8"

    if response.status_code != 200 or not response.text.strip():
        raise ValueError("Không lấy được dữ liệu hoặc dữ liệu rỗng")

    data = response.text.strip().split("o|o")
    result = []
    print(data)

    for item in data:
        fields = item.split("|")
        if len(fields) < 4:
            continue
        result.append(
            OrderLunchResp(
                id_emp=fields[1], name=fields[1], time=fields[2], node=fields[3]
            )
        )

    return result
