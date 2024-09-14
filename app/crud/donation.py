from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def create(
            self,
            object_in,
            user: User,
            session: AsyncSession,
    ):
        object_in_data = object_in.dict()
        if user is not None:
            object_in_data['user_id'] = user.id
        db_object = self.model(**object_in_data)
        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ) -> list[Donation]:
        user_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return user_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
