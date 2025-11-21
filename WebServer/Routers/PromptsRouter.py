from fastapi import APIRouter, HTTPException, status
from Persistence.DTOs import PromptCreate, PromptDelete, PromptRead, PromptUpdate
from Repositories import create_prompt, delete_prompt, get_all_prompts

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"],
)


@router.get("/", tags=["prompts"], response_model=list[PromptRead])
async def read_prompts() -> [PromptRead]:
    try:
        prompts = await get_all_prompts()
        return prompts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/",
    tags=["prompts"],
    response_model=PromptRead,
    response_model_exclude={"hashed_password"},
    status_code=status.HTTP_201_CREATED,
)
async def create_new_prompt(prompt_dto: PromptCreate) -> PromptRead:
    try:
        prompt = await create_prompt(prompt_dto)
        return prompt
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/{id}", tags=["prompts"], response_model=bool)
async def delete_existing_prompt(id: int):

    try:
        success = await delete_prompt(id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
