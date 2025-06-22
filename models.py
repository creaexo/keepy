from typing import NewType

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

StorageId_T = NewType('StorageId_T', int)
"""Тип идентификаторов хранилищ."""


class Base(DeclarativeBase):
    pass


class Storage(Base):
    __tablename__ = 'storage'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    img: Mapped[str] = mapped_column(String(100))


class Item(Base):
    __tablename__ = 'item'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    img: Mapped[str] = mapped_column(String(100))
    storage: Mapped[StorageId_T] = mapped_column(ForeignKey('storage.id', ondelete='RESTRICT'))
    info: Mapped[str] = mapped_column(String(200), nullable=True)
    """Дополнительные информация о предмете, которая поможет его найти, если не помнишь название."""
