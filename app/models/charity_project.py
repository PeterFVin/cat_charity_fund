from sqlalchemy import Column, String, Text

from app.models.base_model import Base_Project_Donation


class CharityProject(Base_Project_Donation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
