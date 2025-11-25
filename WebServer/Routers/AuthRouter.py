import os
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from Persistence.DTOs import UserCreate, UserRead
from Persistence.Enums import USER_ROLE
from Repositories import create_user, delete_user, get_all_users, get_one_user, update_user
from Resources import create_token

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth", "users"],
)

@router.get("/google")
async def auth_google():
    """Generate Google OAuth URL for frontend to redirect to"""
    params = {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "redirect_uri": "http://localhost:8000/auth/google/callback",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
    }
    google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return {"url": google_auth_url}

@router.get("/google/callback")
async def call_back(request: Request) -> str:
    """Handle Google OAuth callback and create/retrieve user"""
    try:
        # Get authorization code from query params
        code = request.query_params.get("code")

        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No authorization code received from Google",
            )

        # Exchange authorization code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                    "redirect_uri": "http://localhost:8000/auth/google/callback",
                    "grant_type": "authorization_code",
                },
            )
            tokens = token_response.json()

        # Check for errors in token response
        if "error" in tokens:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Token exchange failed: {tokens.get('error_description', tokens['error'])}",
            )

        # Get user info from Google
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
            )
            user_info = userinfo_response.json()

        google_id = user_info.get("id")
        google_email = user_info.get("email")
        picture = user_info.get("picture", "")

        if not google_email or not google_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to retrieve required user information from Google",
            )

        this_user = await get_one_user(tmp_id=None, email=google_email)

        if not this_user:
            dto = UserCreate(
                uuid=google_id,
                email=google_email,
                hashed_password="",
                pfp=picture,
                role=USER_ROLE.USER,
            )
            this_user = await create_user(dto)

        user_read = UserRead.model_validate(this_user)
        token = create_token(user_read)
        print(token)
        return RedirectResponse(f"http://localhost:3000/write?jwt={token}")

    except HTTPException:

        raise
    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {e!s}",
        )
