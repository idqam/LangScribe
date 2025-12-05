from Persistence.DTOs import UserCreate, UserUpdate, LanguageRead, ReportRead, UserMessageRead, UserMessageCreate, UserLanguageCreate, UserLanguageRead, UserLanguageUpdate, ReportCreate
from Persistence.Enums import SUBSCRIPTION_TIER
from Persistence.Models import Subscription, User, Language, Report, UserLanguage, UserMessage
from Resources import transaction
from sqlalchemy import delete, select, update
from .UserMessagesRepo import create_usermessage
from .UserLanguagesRepo import create_user_languages, delete_user_languages
from fastapi import status, HTTPException, BackgroundTasks
from Resources import OpenAIClient
from .ReportsRepo import create_report
from .PromptsRepo import get_prompt

async def get_all_users() -> list[User]:
    async with transaction() as session:
        res = await session.execute(
            select(User),
        )

        users: list[User] = res.scalars().all()

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


async def delete_user(id: int) -> int:
    async with transaction() as session:
        user = await session.get(User,id)

        if not user:
            raise ValueError("User not found")

        res = await session.execute(
            delete(User).where(User.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")

        count: int = res.rowcount
    return count


##################### LANGUAGES #######################

async def get_languages(id: int) -> list[UserLanguageRead]:
    async with transaction() as session:
        user = await session.get(User, id)
        return [UserLanguageRead.model_validate(ul) for ul in user.user_languages]
    
async def get_language(user_id: int, ul_id : int) -> UserLanguage:
    async with transaction() as session:
        user = await session.get(User,user_id)
        for lan in user.user_languages:
            if lan.language_id == ul_id:
                return lan
            
    raise Exception("User language not found :/")

async def post_user_language(id: int, user_lan_dto: UserLanguageCreate) -> UserLanguageRead:
    user_lan_dto.user_id = id
    return await create_user_languages(user_lan_dto)

async def patch_user_language(u_id: int,ul_id: int, user_lan_dto: UserLanguageUpdate) -> UserLanguageRead:
    user_lan_dto.user_id = u_id
    async with transaction() as session:
        ul = await session.get(UserLanguage,ul_id)
        if not ul:
            raise ValueError("User Language not found")
        
        session.execute(
            update(UserLanguage).values(**user_lan_dto.model_dump())
        )

        await session.flush()
        await session.refresh(ul)
        
    return ul

async def delete_my_user_language(id: int, delete_id: int) -> bool:
    async with transaction() as session:
        user = await session.get(User,id)
        if not user:
            raise ValueError("User not found")
        
        language = await session.get(UserLanguage,delete_id)
        
        if id != language.user_id:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only operate on your own resources.",
        )
    success: int = await delete_user_languages(delete_id)
    return bool(success)

################ REPORTS ##########################
    
async def get_reports(id: int) -> list[ReportRead]:
    async with transaction() as session:
        user = await session.get(User,id)
        return [ReportRead.model_validate(report) for report in user.reports]
    

async def retry_reports(message_id: int, user_id: int, background_task: BackgroundTasks) -> list[ReportRead]:
    async with transaction() as session:
        user = await session.get(User,user_id)
        message = await session.get(UserMessage,id)
        prompt = await get_prompt(message.prompt_id)
        user_language = await get_language(user.id,prompt.language_id)

        exist = False

        for message in user.messages:
            if message.id == message_id:
                exist = True

        if not exist:
            raise Exception('message not found!')
        
        async def bg_create_report():
            ai_response = OpenAIClient().review_user_text(
                user_text= message.content,
                prompt= prompt.content,
                user_language=user.default_language,
                user_proficiency=user_language.proficiency_level
            )

            report = ReportCreate(
                user_id=user.id,
                user_message_id=message.id,
                content=ai_response,
                language_id= user_language.language_id,
                rating=3
            )

            await create_report(report)
        
    background_task.add_task(bg_create_report)
        


################ MESSAGES #############################
    
async def get_messages(id: int) -> list[UserMessageRead]:
    async with transaction() as session:
        user = await session.get(User,id)
        return [UserMessageRead.model_validate(message) for message in user.messages]
    
async def post_message(id: int, message_dto: UserMessageCreate) -> UserMessageRead:
    message_dto.user_id = id


    return await create_usermessage(message_dto)







