from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.users import Users
from models import get_db
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> Users:
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in token")
        
        # Fetch the user from the database
        user = session.query(Users).filter(Users.id == user_id, Users.deleted_at.is_(None)).first()
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")