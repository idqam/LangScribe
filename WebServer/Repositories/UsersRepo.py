from Persistence.DTOs import UserCreate, UserUpdate, LanguageRead, ReportRead
from Persistence.Enums import SUBSCRIPTION_TIER
from Persistence.Models import Subscription, User, Language, Report
from Resources import transaction
from sqlalchemy import delete, select, update
import asyncio

async def get_all_users() -> [User]:
    async with transaction() as session:
        res = await session.execute(
            select(User),
        )

        users = res.scalars().all()

    return users


async def get_one_user(tmp_id: int | None, email: str | None) -> User:
    async with transaction() as session:
        if tmp_id:
            user = await session.execute(
                select(User).where(User.id == tmp_id),
            )

        else:
            user = await session.execute(
                select(User).where(User.email == email),
            )

    return user.scalar_one_or_none()


async def update_user(tmp_id: int, tmp_user: UserUpdate) -> User:
    async with transaction() as session:
        user = await session.get(User, tmp_id)

        if not user:
            raise ValueError("User not found")

        res = await session.execute(
            update(User).where(User.id == tmp_id).values(**tmp_user.model_dump(exclude_unset=True)),
        )

        if res.rowcount == 0:
            raise ValueError("Update failed - no rows affected")

    return res.rowcount


async def create_user(tmp_user: UserCreate) -> User:
    async with transaction() as session:
        user = await session.execute(
            select(User).where(User.email.ilike(tmp_user.email)),
        )

        if user.one_or_none():
            raise ValueError("User already registered")


        res = await session.execute(
            select(Subscription).where(Subscription.tier == SUBSCRIPTION_TIER.FREE),
        )
        subs_id = res.scalar_one_or_none().id
        if not subs_id:
            raise ValueError("Free Tier not found")

        user_data = tmp_user.model_dump()
        user_data["subscription_id"] = subs_id
        new_user = User(**user_data)

        session.add(new_user)
        await session.flush()
        await session.refresh(new_user)

    return new_user


async def delete_user(id: int) -> bool:
    async with transaction() as session:
        user = await session.get(User,id)

        if not user:
            raise ValueError("User not found")

        res = await session.execute(
            delete(User).where(User.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")


    return res.rowcount

async def get_languages(id: int) -> list[LanguageRead]:
    async with transaction() as session:
        user = await session.get(User, id)
        return [LanguageRead.model_validate(ul.language) for ul in user.user_languages]
    
async def get_reports(id: int) -> list[ReportRead]:
    async with transaction() as session:
        user = await session.get(User,id)
        return [ReportRead.model_validate(report) for report in user.reports]