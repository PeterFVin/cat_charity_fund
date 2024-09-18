from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_model import BaseAbstractModel


class Donation(BaseAbstractModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
