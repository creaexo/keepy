from typing import NewType

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

StorageName_T = NewType('StorageName_T', str)
"""Тип имени хранилищ."""


class Base(DeclarativeBase):
    pass


class Storage(Base):
    __tablename__ = 'storage'
    name: Mapped[str] = mapped_column(String(30), primary_key=True)
    img: Mapped[str] = mapped_column(String(100), nullable=True)


class Item(Base):
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    storage: Mapped[StorageName_T] = mapped_column(ForeignKey('storage.name', ondelete='RESTRICT'))
    img: Mapped[str] = mapped_column(String(100), nullable=True)
    info: Mapped[str] = mapped_column(String(200), nullable=True)
    """Дополнительные информация о предмете, которая поможет его найти, если не помнишь название."""
