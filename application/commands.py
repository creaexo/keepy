from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from application.models import Item, Storage, StorageName_T


async def create_storage(session: AsyncSession, name: str, img_path: str) -> Storage:
    stmt = insert(Storage).values(name=name, img=img_path).returning(Storage)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one()


async def create_item(
    session: AsyncSession,
    name: str,
    img_path: str,
    storage_id: StorageName_T,
    info: str | None = None,
) -> Item:
    # fmt: off
    stmt = (
        insert(Item)
        .values(name=name, img=img_path, storage=storage_id, info=info)
        .returning(Item)
    )
    # fmt: on
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one()
