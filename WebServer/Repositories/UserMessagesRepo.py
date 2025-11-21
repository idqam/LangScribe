from Persistence.DTOs import UserMessageCreate
from Persistence.Models import Prompt, UserMessage
from Resources import transaction
from sqlalchemy import delete, select


async def get_all_usermessages() -> [UserMessage]:
    async with transaction() as session:
        res = await session.execute(
            select(UserMessage),
        )

        usermessages = res.scalars().all()

    return usermessages


async def create_usermessage(tmp_usermessage: UserMessageCreate) -> UserMessage:
    async with transaction() as session:

        prompt = await session.get(Prompt,tmp_usermessage.prompt_id)

        if not prompt:
            raise ValueError("Prompt not found!")

        new_usermessage = UserMessage(**tmp_usermessage.model_dump())
        session.add(new_usermessage)
        await session.flush()
        await session.refresh(new_usermessage)

    return new_usermessage


async def delete_usermessage(id: int) -> bool:
    async with transaction() as session:
        usermessage = await session.get(UserMessage,id)

        if not usermessage:
            raise ValueError("UserMessage not found")

        res = await session.execute(
            delete(UserMessage).where(UserMessage.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")


    return res.rowcount
