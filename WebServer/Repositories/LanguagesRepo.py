from Persistence.DTOs import LanguageCreate, LanguageDelete, LanguageUpdate
from Persistence.Models import Subscription, Language
from Resources import transaction
from sqlalchemy import delete, insert, select, update
from loguru import logger

async def get_all_languages() -> [Language]:
    async with transaction() as session:
        res = await session.execute(
            select(Language),
        )

        languages = res.scalars().all()

    return languages


async def get_one_language(tmp_id: int | None) -> Language:
    async with transaction() as session:

        language = await session.execute(
            select(Language).where(Language.id == tmp_id),
        )

        if not language.scalar_one_or_none():
            raise ValueError("Language not found")

    return language.scalar_one_or_none()


async def update_language(tmp_id: int, tmp_language: LanguageUpdate) -> Language:
    async with transaction() as session:
        language = await session.get(Language, tmp_id)

        if not language:
            raise ValueError("Language not found")

        res = await session.execute(
            update(Language).where(Language.id == tmp_id).values(**tmp_language.model_dump(exclude_unset=True)),
        )

        if res.rowcount == 0:
            raise ValueError("Update failed - no rows affected")

    return res.rowcount


async def create_language(tmp_language: LanguageCreate) -> Language:
    async with transaction() as session:

        language = await session.execute(
            select(Language).where(Language.name.ilike(tmp_language.name)),
        )

        if language.one_or_none():
            raise ValueError("Language already registered")

        new_language = Language(**tmp_language.model_dump())
        session.add(new_language)
        await session.flush()
        await session.refresh(new_language)
        
    return new_language


async def delete_language(id: int) -> bool:
    async with transaction() as session:
        language = await session.get(Language,id)

        if not language:
            raise ValueError("Language not found")

        res = await session.execute(
            delete(Language).where(Language.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")


    return res.rowcount
