from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.schemas.auth import UserCreate, UserOut, Token
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_current_user
from app.core.limiter import limiter

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
@limiter.limit("5/hour")
def register(request: Request, user_in: UserCreate, db: Session = Depends(get_db)):
    if len(user_in.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 8 characters."
        )
    if user_in.password.isdigit():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password cannot be numbers only."
        )
    if user_in.password.lower() in ("password", "12345678", "qwerty123",
                                     "password123", "abc12345"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password is too common."
        )

    if len(user_in.username) < 3:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username must be at least 3 characters."
        )
    if not user_in.username.replace("_", "").replace("-", "").isalnum():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username can only contain letters, numbers, hyphens and underscores."
        )

    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(400, "Username already registered")

    user = User(username=user_in.username, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
@limiter.limit("10/hour")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
