from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Annotated
from fastapi.openapi.models import APIKey
from app.models.database import get_user, verify_password
from app.models.sessions import create_or_update_session, get_session, invalidate_session, is_session_expired

router = APIRouter()

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=8, max_length=128)

@router.post("/login", summary="User login")
def login(request: LoginRequest):
    user = get_user(request.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # Create session token
    token, expiration = create_or_update_session(request.username)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_at": expiration
    }

@router.post("/refresh", summary="Refresh an access token")
def refresh_token(authorization: str = Header(...)):
    token = authorization.split(" ")[1] if " " in authorization else authorization
    session = get_session(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

     # Check maximum session lifetime
    if is_session_expired(session):
        raise HTTPException(status_code=401, detail="Session expired. Please log in again.")

    # Update the session expiration
    _, expiration = create_or_update_session(token)

    return {
        "access_token": token,  # Return the same token
        "token_type": "bearer",
        "expires_at": expiration,
    }

@router.post(
    "/logout",
    summary="Log out and invalidate a token",
    description="Log out by providing a valid Bearer token in the Authorization header.",
    responses={
        200: {"description": "Logged out successfully"},
        401: {"description": "Invalid or expired token"},
    }
)
def logout(
    authorization: Annotated[str, Header(..., description="Bearer token for the session")]
):
    token = authorization.split(" ")[1] if " " in authorization else authorization
    session = get_session(token)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    invalidate_session(token)
    return {"detail": "Logged out successfully"}
