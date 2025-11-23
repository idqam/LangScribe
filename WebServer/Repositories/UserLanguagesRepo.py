from Persistence.DTOs import UserLanguageCreate
from Persistence.Models import Language, User, UserLanguage
from Resources import self_user, transaction
from sqlalchemy import delete, select


async def get_all_user_languages() -> [UserLanguage]:
    async with transaction() as session:
        res = await session.execute(
            select(UserLanguage),
        )


        user_languages = res.scalars().all()

    return user_languages


async def create_user_languages(tmp_user_languages: UserLanguageCreate) -> UserLanguage:
    async with transaction() as session:

        language = await session.get(Language,tmp_user_languages.language_id)
        user = await session.get(User, tmp_user_languages.user_id)

        if not language or not user:
            raise ValueError("User or Language not found!")

        new_user_languages = UserLanguage(**tmp_user_languages.model_dump())
        session.add(new_user_languages)
        await session.flush()
        await session.refresh(new_user_languages)

    return new_user_languages


async def delete_user_languages(id: int,user_id:int) -> bool:
    async with transaction() as session:
        user_languages = await session.get(UserLanguage,id)


        if not user_languages:
            raise ValueError("UserLanguage not found")

        res = await session.execute(
            delete(UserLanguage).where(UserLanguage.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")


    return res.rowcount
