from typing import Optional
from datetime import datetime

from pydantic import ConfigDict, NonNegativeInt, BaseModel


class DonationCreate(BaseModel):
    full_amount: NonNegativeInt
    comment: Optional[str] = None


class DonationDBCreate(DonationCreate):
    id: int
    create_date: datetime
    model_config = ConfigDict(from_attributes=True)


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime] = None
