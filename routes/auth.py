from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.user import User
from .schemas import SignupRequest
from db.database import get_db
from sqlalchemy.orm import Session
from util.hasher import hash_password, compare_passwords
from util.jwt import generate_tokens, validate_token

auth_router = APIRouter(prefix="/auth")

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), is_refresh: bool = False):
    token = credentials.credentials
    print(token)
    try:
        user_data = validate_token(token[7:], is_refresh)
        return user_data
    except ValueError as e:
        raise HTTPException(401, f"Error: {e}")
    
def get_current_user_with_refresh(credentials: HTTPAuthorizationCredentials = Security(security)):
    return get_current_user(credentials, is_refresh=True)




@auth_router.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(400, "Username already exists")
    new_user = User(username = request.username, password=hash_password(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


@auth_router.post("/login")
def login(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user and compare_passwords(request.password, existing_user.password):
        return generate_tokens({"id": existing_user.id, "username": existing_user.username, "role": existing_user.role})
    raise HTTPException(400, "Bad credentials")


@auth_router.post("/refresh-token")
def refresh_token(user_data: dict = Depends(get_current_user_with_refresh)):
    new_token = generate_tokens({"id": user_data["id"], "username": user_data["username"], "role": user_data["role"]})
    return {"access_token":new_token["access_token"]}


@auth_router.get("/profile")
def get_profile(user_data: dict = Depends(get_current_user)):
    return {"username": user_data["username"], "role": user_data["role"]}