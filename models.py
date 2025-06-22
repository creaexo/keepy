from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Storage(Base):
    __tablename__ = 'storage'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    img: Mapped[str] = mapped_column(String(100))

