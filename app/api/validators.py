from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectUpdate


async def check_unique_name(
        project_name: str,
        session: AsyncSession
):
    project_id = await charity_project_crud.get_project_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
):
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект с указанным айли не найден!'
        )
    return project


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get(project_id, session)
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return project


async def check_project_closed(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Проект закрыт, не подлежит изменению!',
        )


async def check_edit_sum(
        project_id: int,
        project: CharityProjectUpdate,
        session: AsyncSession
):
    project_old = await charity_project_crud.get(project_id, session)
    if project.full_amount is not None:
        if project.full_amount < project_old.invested_amount:
            raise HTTPException(
                status_code=400,
                detail='Нелья установить значение'
                ' full_amount меньше уже вложенной суммы',
            )
        elif project.full_amount == project_old.invested_amount:
            project_old.fully_invested = True
            project_old.close_date = datetime.now()
            session.add(project_old)
            await session.commit()
            await session.refresh(project_old)
