from fastapi import APIRouter

router = APIRouter(
    prefix="/prompts",
    tags=["prompts"],
)


@router.get("/prompts/", tags=["prompts"])
async def read_prompts():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/prompts/", tags=["prompts"])
async def create_prompts():
    return {"username": "fakecurrentuser"}


@router.put("/prompts/{prompt}", tags=["prompts"])
async def update_prompts(username: str):
    return {"username": username}


@router.delete("/prompts/{prompts}", tags=["prompts"])
async def delete_prompts(username: str):
    return {"username": username}
