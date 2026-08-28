from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, select

from dependencies.database import SessionDep
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserUpdate(SQLModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserPublic(SQLModel):
    id: int
    username: str
    email: str


@router.post("/", response_model=UserPublic, status_code=201)
def create_user(user_data: UserCreate, session: SessionDep):
    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=list[UserPublic])
def read_users(session: SessionDep):
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_data: UserUpdate, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    session.delete(user)
    session.commit()
