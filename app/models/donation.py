from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_model import Base_Project_Donation


class Donation(Base_Project_Donation):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
