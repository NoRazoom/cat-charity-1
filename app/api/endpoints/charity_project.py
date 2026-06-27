from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.charity_project import (CharityProjectDB,
                                         CharityProjectCreate,
                                         CharityProjectUpdate)
from app.crud.charity_project import charity_project_crud
from app.api.validators import (check_unique_name, check_project_before_delete,
                                check_project_exists, check_project_closed,
                                check_edit_sum)


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(session: SessionDep):
    """Показать список всех целевых проектов."""
    projects = await charity_project_crud.get_multi(session)
    return projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def create_new_project(
    project: CharityProjectCreate,
    session: SessionDep
):
    """Создать целевой проект."""
    await check_unique_name(project.name, session)
    project = await charity_project_crud.create(project, session)
    project = await charity_project_crud.investition(project.id, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def remove_project(
    project_id: int,
    session: SessionDep
):
    """
    Удалить целевой проект.
    Нельзя удалить проект, в который уже были инвестированы средства.
    """
    project = await check_project_exists(project_id, session)
    project = await check_project_before_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: SessionDep
):
    """
    Редактировать целевой проект.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_unique_name(obj_in.name, session)
    await check_project_closed(project_id, session)
    project = await check_edit_sum(project_id, obj_in, session)
    if (obj_in.full_amount is not None and
            project.invested_amount == obj_in.full_amount):
        project.fully_invested = True
        project.close_date = datetime.now()
        session.add(project)
        await session.commit()
        await session.refresh(project)

    project = await charity_project_crud.update(project, obj_in, session)
    return project
