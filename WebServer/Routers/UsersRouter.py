from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from Persistence.DTOs import (
    ReportRead,
    UserLanguageCreate,
    UserLanguageRead,
    UserMessageCreate,
    UserMessageRead,
    UserRead,
    UserUpdate,
    UserLanguageUpdate,
    ReportCreate
)
from Repositories import (
    delete_my_user_language,
    delete_user,
    get_languages,
    get_one_user,
    get_reports,
    post_message,
    post_user_language,
    update_user,
    patch_user_language,
    get_messages,
    create_report,
    get_prompt,
    get_language,
    retry_reports
)
from Resources import verify_token, lifespan, OpenAIClient

router = APIRouter(
    prefix="/users/me",
    tags=["users"],
    lifespan=lifespan
)


@router.get("/", response_model=UserRead)
async def get_me(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_one_user(token_data.id, token_data.email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.patch("/update")
async def update_me(update_data: UserUpdate,token_data: UserRead = Depends(verify_token)):
    try:
        success = await update_user(token_data.id, update_data)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.delete("/delete")
async def delete_me(token_data: UserRead = Depends(verify_token)):
    try:
        success = await delete_user(token_data.id)
        return bool(success)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

################ LANGUAGES ###################################33

@router.get("/languages", response_model=list[UserLanguageRead])
async def get_my_languages(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_languages(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/languages", response_model=UserLanguageRead)
async def post_my_languages(user_language: UserLanguageCreate,token_data: UserRead = Depends(verify_token)):
    try:
        return await post_user_language(user_lan_dto=user_language,id=token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.patch("/languages/{id}", response_model=UserLanguageRead)
async def patch_my_language(id: int,user_language: UserLanguageUpdate,token_data: UserRead = Depends(verify_token)):
    try:
        return await patch_user_language(token_data.id,id,user_language)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/languages/{id}", response_model=bool)
async def delete_my_language(id: int, token_data: UserRead = Depends(verify_token)):
    try:
        success = await delete_my_user_language(token_data.id,id)
        return bool(success)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

################### REPORT ###########################

@router.get("/reports", response_model=list[ReportRead])
async def get_my_reports(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_reports(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    
@router.get('/reports/re-try/{message_id}',response_model=None)
async def retry_report(message_id: int, background_task: BackgroundTasks,token_data: UserRead = Depends(verify_token)):

    await retry_reports(message_id=message_id, user_id=token_data.id,background_task=background_task )



################## MESSAGES ##########################

@router.get("/messages", response_model=list[UserMessageRead])
async def get_my_messages(token_data: UserRead = Depends(verify_token)):
    try:
        return await get_messages(token_data.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("/messages", response_model=UserMessageCreate)
async def post_add_message(message: UserMessageCreate, background_task: BackgroundTasks,token_data: UserRead = Depends(verify_token)):
    try:
        message = await post_message(token_data.id,message)
        prompt = await get_prompt(message.prompt_id)
        user_language = await get_language(token_data.id,prompt.language_id)

        async def bg_create_report():
            ai_response = OpenAIClient().review_user_text(
                user_text= message.content,
                prompt= prompt.content,
                user_language=token_data.default_language,
                user_proficiency=user_language.proficiency_level
            )

            report = ReportCreate(
                user_id=token_data.id,
                user_message_id=message.id,
                content=ai_response,
                language_id= user_language.language_id,
                rating=3 ##TODO: Extract from ai_response.rate or something like that
            )

            await create_report(report)

        background_task.add_task(bg_create_report)
        
        return message
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
