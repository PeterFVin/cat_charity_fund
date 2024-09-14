from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def func_donation(
        session: AsyncSession,
        object,
):
    open_projects = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == 0
    ).order_by(CharityProject.create_date))
    project = open_projects.scalars().first()

    open_donations = await session.execute(select(Donation).where(
        Donation.fully_invested == 0
    ).order_by(Donation.create_date))
    donation = open_donations.scalars().first()

    while project and donation:

        project_sum_left = project.full_amount - project.invested_amount
        balance_sum_left = donation.full_amount - donation.invested_amount

        if project_sum_left > balance_sum_left:
            project.invested_amount += balance_sum_left
            donation.invested_amount += balance_sum_left
            donation.fully_invested = True
            donation.close_date = datetime.now()

        elif project_sum_left == balance_sum_left:
            project.invested_amount += balance_sum_left
            donation.invested_amount += balance_sum_left
            project.fully_invested = donation.fully_invested = True
            project.close_date = datetime.now()
            donation.close_date = datetime.now()

        elif project_sum_left < balance_sum_left:
            project.invested_amount += project_sum_left
            donation.invested_amount += project_sum_left
            project.fully_invested = True
            project.close_date = datetime.now()

        session.add(project)
        session.add(donation)
        await session.commit()
        await session.refresh(project)
        await session.refresh(donation)

        open_projects = await session.execute(select(CharityProject).where(
            CharityProject.fully_invested == 0
        ).order_by(CharityProject.create_date))
        project = open_projects.scalars().first()

        open_donations = await session.execute(select(Donation).where(
            Donation.fully_invested == 0
        ).order_by(Donation.create_date))
        donation = open_donations.scalars().first()

    await session.refresh(object)
    return object
