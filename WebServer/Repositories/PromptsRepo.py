from Persistence.DTOs import PromptCreate
from Persistence.Models import Language, Prompt
from Resources import transaction
from sqlalchemy import delete, select


async def get_all_prompts() -> list[Prompt]:
    async with transaction() as session:
        res = await session.execute(
            select(Prompt),
        )

        prompts:list[Prompt]  = res.scalars().all()

    return prompts

async def get_prompt(id: int) -> Prompt:

    async with transaction() as session:
        res = await session.get(Prompt,id)

    return res 


async def create_prompt(tmp_prompt: PromptCreate) -> Prompt:
    async with transaction() as session:

        language = await session.get(Language,tmp_prompt.language_id)

        if not language:
            raise ValueError("Language not found!")

        new_prompt = Prompt(**tmp_prompt.model_dump())
        session.add(new_prompt)
        await session.flush()
        await session.refresh(new_prompt)

    return new_prompt


async def delete_prompt(id: int) -> int:
    async with transaction() as session:
        prompt = await session.get(Prompt,id)

        if not prompt:
            raise ValueError("Prompt not found")

        res = await session.execute(
            delete(Prompt).where(Prompt.id == id),
        )

        if not res.rowcount:
            raise ValueError("No rows were affected")

        count: int = res.rowcount
    return count
