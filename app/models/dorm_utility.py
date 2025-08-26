# app/models/dorm_utility.py
from sqlalchemy import String, Float, Integer, Text, Date, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import date


class DormUtility(Base):
    """
    Bảng thống kê phí ký túc xá (1 dòng = 1 hộ/nhân viên trong 1 kỳ).
    """
    __tablename__ = "dorm_utility"

    # PK
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ===== Metadata của kỳ báo cáo (header) =====
    period_month: Mapped[date] = mapped_column(Date, nullable=False, index=True)  # Kỳ: ngày đầu tháng (e.g. 2025-08-01)

    # ===== Thông tin hộ/nhân viên =====
    dorm_no: Mapped[str | None] = mapped_column(String(20), index=True)       # 宿舍編號
    employee_id: Mapped[str | None] = mapped_column(String(20), index=True)   # 人員代號
    employee_name: Mapped[str | None] = mapped_column(String(100))            # 姓名

    # ===== 用電 (điện) =====
    elec_prev_read: Mapped[int | None] = mapped_column(Integer)               # 上月度數
    elec_curr_read: Mapped[int | None] = mapped_column(Integer)               # 本月度數
    elec_usage:     Mapped[int | None] = mapped_column(Integer)               # 用電度數
    elec_amount:    Mapped[int | None] = mapped_column(BigInteger)            # 用電金額

    # ===== 用水 (nước) =====
    water_prev_read: Mapped[int | None] = mapped_column(Integer)              # 上月度數
    water_curr_read: Mapped[int | None] = mapped_column(Integer)              # 本月度數
    water_usage:     Mapped[int | None] = mapped_column(Integer)              # 用水度數
    water_amount:    Mapped[int | None] = mapped_column(BigInteger)           # 用水金額

    # ===== Phí khác & tổng =====
    shared_fee:   Mapped[int | None] = mapped_column(BigInteger)              # 分攤費
    cleaning_fee: Mapped[int | None] = mapped_column(BigInteger)              # 清潔管理費
    total_amount: Mapped[int | None] = mapped_column(BigInteger)              # 總金額
