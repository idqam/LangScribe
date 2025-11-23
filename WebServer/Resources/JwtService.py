import os
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from Persistence.DTOs import UserRead
from Persistence.Enums import USER_ROLE

app = FastAPI()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()
def create_token(user: UserRead) -> str:
    to_encode = user.model_dump()
    expire = datetime.now(UTC) + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserRead:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return UserRead(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def authorize_user_operation(
    user: UserRead,
    required_role: USER_ROLE,
):

    if user.role == USER_ROLE.ADMIN:
        return
    #in case theres more roles
    if user.role < required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permission level.",
        )

def admin_required(user: UserRead = Depends(verify_token)):
    authorize_user_operation(user, required_role=USER_ROLE.ADMIN)

def self_user(user: UserRead, current_user: UserRead):
    authorize_user_operation(user, required_role=USER_ROLE.USER)
    if user.id is not None and current_user.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only operate on your own resources.",
        )





