from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (
    check_charity_project_exists,
    check_delete_project_invested,
    check_delete_project_closed,
    check_name_duplicate,
    check_update_project_closed,
    check_update_project_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.invest_funcs import func_donation

CHARITY_CREATE_ERROR_MESSAGE = 'Необходимо заполнить все поля!'


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    if charity_project.name is None or charity_project.description is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=CHARITY_CREATE_ERROR_MESSAGE
        )
    await check_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session
    )
    return await func_donation(session, new_charity_project)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_charity_project_all(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    await check_update_project_closed(project_id, session)
    if obj_in.full_amount:
        await check_update_project_invested(
            charity_project, obj_in.full_amount
        )
    return await charity_project_crud.update(
        charity_project, obj_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_delete_project_closed(project_id, session)
    await check_delete_project_invested(project_id, session)
    return await charity_project_crud.remove(
        charity_project, session
    )
