from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import get_db
from models.users import Users
from schemas.users import UserCreate, Token, TokenData
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
import os

router = APIRouter(prefix="", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/users", response_model=Token)
async def register_users(user: UserCreate, session: Session = Depends(get_db)):
    # Check if username already exists
    db_user = Users.find(session=session, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create a new user
    new_user = Users.create(session, user)
    
    # Generate JWT token for the new user
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60)))
    access_token = Users.create_access_token(
        data={"sub": new_user.username, "user_id": new_user.id}, expires_delta=access_token_expires
    )
    
    # Return token and username
    return {"access_token": access_token, "token_type": "bearer", "username": new_user.username}


@router.post("/token", response_model=Token)
async def login_for_access_token(formdata: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = Users().authenticate_user(session, formdata.username, formdata.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 60)))
    access_token = Users.create_access_token(
        data={"sub": user.username, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "username": user.username}

@router.get("/me", response_model=TokenData)
async def fetch_me(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = Users.find(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return {
        "username": user.username,
        "total_points": user.total_points
    }


@router.put("/update-bank-details")
async def update_bank_details(bank_name: str, account_number: str, ifsc_code: str, branch_name: str, account_type: str, token: str = Depends(oauth2_scheme), session: Session = Depends(get_db),):
    return Users.update_bank_details(session, token, bank_name, account_number, ifsc_code, branch_name, account_type)


@router.get("/bank-details")
async def get_bank_details(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    return Users.get_bank_details(session, token)

