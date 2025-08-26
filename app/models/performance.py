# app/models/performance.py
from sqlalchemy import String, Float, Integer, Text, Date
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import date

class Performance(Base):
    __tablename__ = "performance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    eval_year_month: Mapped[date] = mapped_column(Date, nullable=False)  # 評核年月
    employee_id: Mapped[str] = mapped_column(String(20), index=True)  # 工號
    employee_name: Mapped[str] = mapped_column(String(100))    # 姓名
    grade: Mapped[str] = mapped_column(String(50))             # 職等
    nationality: Mapped[str] = mapped_column(String(10))       # 國籍
    dept_code: Mapped[str] = mapped_column(String(20))         # 部門代碼
    dept_name: Mapped[str] = mapped_column(String(100))        # 部門名稱
    rank_code6: Mapped[str] = mapped_column(String(20))        # 職等六碼
    rank_name: Mapped[str] = mapped_column(String(100))        # 職等名稱

    first_score: Mapped[str | None] = mapped_column(String(20))    # 初核成績
    first_comment: Mapped[str | None] = mapped_column(Text)        # 初核評語
    first_supervisor: Mapped[str | None] = mapped_column(String(50))

    review_score: Mapped[str | None] = mapped_column(String(20))   # 複核成績
    review_comment: Mapped[str | None] = mapped_column(Text)
    review_supervisor: Mapped[str | None] = mapped_column(String(50))

    final_score: Mapped[str | None] = mapped_column(String(20))    # 核定成績
    final_comment: Mapped[str | None] = mapped_column(Text)
    final_supervisor: Mapped[str | None] = mapped_column(String(50))

    mgr_first_score: Mapped[str | None] = mapped_column(String(20))   # 經理室初核成績
    mgr_first_comment: Mapped[str | None] = mapped_column(Text)
    mgr_first_supervisor: Mapped[str | None] = mapped_column(String(50))

    mgr_review_score: Mapped[str | None] = mapped_column(String(20))
    mgr_review_comment: Mapped[str | None] = mapped_column(Text)
    mgr_review_supervisor: Mapped[str | None] = mapped_column(String(50))

    mgr_final_score: Mapped[str | None] = mapped_column(String(20))
    mgr_final_comment: Mapped[str | None] = mapped_column(Text)
    mgr_final_supervisor: Mapped[str | None] = mapped_column(String(50))

    leave_days_total: Mapped[float | None] = mapped_column(Float)   # 請假總日數
