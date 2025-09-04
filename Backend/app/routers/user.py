from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.db_setup import get_db
from ..schemas.user import UserRegisterSchema, UserOutSchema
from ..models.auth import User

router = APIRouter(tags=["user"], prefix="/user")

@router.post("/register", response_model=UserOutSchema)
async def register_user(user: UserRegisterSchema, db: Session = Depends(get_db)):
    pass