from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.donation import DonationDB, DonationCreate, DonationDBCreate
from app.crud.donation import donation_crud


router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_all_donations(session: SessionDep):
    """Показать список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationDBCreate,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep
):
    """Создать пожертвование."""
    donation = await donation_crud.create(donation, session)
    return await donation_crud.investition(donation.id, session)
