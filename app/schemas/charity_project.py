from typing import Optional
from datetime import datetime

from pydantic import ConfigDict, NonNegativeInt, Field, BaseModel


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    full_amount: Optional[NonNegativeInt] = None


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=10)
    full_amount: int = Field(..., gt=0)
    model_config = ConfigDict(extra='forbid')


class CharityProjectUpdate(CharityProjectBase):
    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None
    model_config = ConfigDict(
        from_attributes=True,
    )
