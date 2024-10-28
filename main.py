from fastapi import FastAPI, Path, status, Body, HTTPException
from pydantic import BaseModel
from typing import List

# uvicorn main:app
app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/users")
def get_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}")
def create_user(username: str, age: int) -> User:
    user_id = len(users) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: int, username: str, age: int) -> User:
    try:
        for user in users:
            if user.id == user_id:
                user.username = username
                user.age = age
                return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
def delete_user(user_id: int) -> User:
    try:
        user_del = users.pop(user_id - 1)
        return user_del
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
