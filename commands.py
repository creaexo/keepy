from pathlib import Path

from sqlalchemy import insert
from sqlalchemy.orm import Session

from models import Storage, Item, StorageId_T


def create_storage(session: Session, name: str, img: Path) -> None:
    session.execute(
        insert(Storage)
        .values(name=name, img=img)
    )
    session.commit()


def create_item(
    session: Session,
    name: str,
    img: Path,
    storage: StorageId_T,
    info: str | None = None
) -> None:
    session.execute(
        insert(Item)
        .values(name=name, img=img, storage=storage, info=info)
    )
    session.commit()
