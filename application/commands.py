from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Storage, Item, StorageId_T


async def create_storage(
    session: AsyncSession, name: str, img_path: str
) -> Storage:
    stmt = insert(Storage).values(name=name, img=img_path).returning(Storage)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one()


async def create_item(
    session: AsyncSession,
    name: str,
    img_path: str,
    storage_id: StorageId_T,
    info: str | None = None
) -> Item:
    stmt = insert(Item).values(
        name=name, img=img_path, storage=storage_id, info=info
    ).returning(Item)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one()
