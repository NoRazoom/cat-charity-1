from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text

from app.core.db import Base, CatMixin


class Donation(CatMixin, Base):
    comment: Mapped[str] = mapped_column(Text, nullable=True)
