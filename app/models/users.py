from sqlalchemy import Column, Integer, String, DateTime, Float
from fastapi import Depends, HTTPException, status
from models import Base
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from schemas.users import UserResponse, UserCreate
from sqlalchemy.orm import relationship, Session
import os


class Users(Base):
    __tablename__ = "users"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())
    deleted_at = Column(DateTime, nullable=True)

    # Bank details fields
    bank_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True, unique=True)
    ifsc_code = Column(String, nullable=True)
    branch_name = Column(String, nullable=True)
    account_type = Column(String, nullable=True)  # e.g., "savings", "checking"

    # Points field to keep track of total points
    total_points = Column(Float, default=0)

    # Relationship with Points model
    points_history = relationship("Points", back_populates="user", cascade="all, delete-orphan")

    @classmethod
    def find(cls, session, username: str):
        return session.query(cls).filter_by(username=username, deleted_at=None).first()

    @classmethod
    def create(cls, session, user: UserCreate):
        hashed_password = cls.pwd_context.hash(user.password)
        new_user = cls(
            username=user.username,
            password=hashed_password
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return UserResponse(id=new_user.id, username=new_user.username)

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return Users.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, session, username: str, password: str):
        user = self.find(session, username)
        if not user or not self.verify_password(password, user.password):
            return False
        return user

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
        return encoded_jwt


    @classmethod
    def update_bank_details(cls, session: Session, token: str, bank_name: str, account_number: str, ifsc_code: str, branch_name: str, account_type: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        # Decode the token to extract user information
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        # Find the user by username
        user = session.query(cls).filter_by(username=username, deleted_at=None).first()
        if user is None:
            raise credentials_exception
        
        # Update bank details
        user.bank_name = bank_name
        user.account_number = account_number
        user.ifsc_code = ifsc_code
        user.branch_name = branch_name
        user.account_type = account_type
        
        # Commit the changes to the database
        session.commit()
        session.refresh(user)
        
        return {"message": "Bank details updated successfully", "username": user.username}

    @classmethod
    def get_bank_details(cls, session: Session, token: str):
        # Exception for invalid credentials
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        # Decode the token to extract user information
        try:
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        # Find the user by username
        user = session.query(cls).filter_by(username=username, deleted_at=None).first()
        if user is None:
            raise credentials_exception
        
        # Return bank details
        return {
            "bank_name": user.bank_name,
            "account_number": user.account_number,
            "ifsc_code": user.ifsc_code,
            "branch_name": user.branch_name,
            "account_type": user.account_type
        }