from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..schemas.users import UserRead, UserCreate
from ..services.users import UserService
from ..repositories.users import UserRepository
from ..database import get_db
from ..models.users import User

router = APIRouter()

# Dependency injection for database session and service
def get_user_service(db: Session = Depends(get_db)):
    return UserService(UserRepository(db))

@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        user = user_service.create(obj_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
