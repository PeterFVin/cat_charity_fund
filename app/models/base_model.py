from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BaseModel(Base):
    """Базовая абстрактная модель для моделей CharityProject и Donation."""
    __abstract__ = True

    full_amount = Column(Integer,
                         CheckConstraint('full_amount > 0'),
                         nullable=False)
    invested_amount = Column(Integer,
                             CheckConstraint('invested_amount >= 0'),
                             default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
