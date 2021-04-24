import logging
from http import HTTPStatus

import Helper
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from CassandraModels import users
from fastapi import APIRouter, HTTPException, Request
from models import Detail, User

UserRouter: APIRouter = APIRouter(tags=["Users"])

_hasher = PasswordHasher()
_userLogger: logging.Logger = logging.getLogger("user")


@UserRouter.options(path="/user/{username}")  # TODO: Create OpenAPI docs
def usernameExists(username: str):
    query = users.objects(username=username)
    if query.count() > 0:
        return {"detail": "Username Exists", "Exists": True}
    return {"detail": "Username doesn't exist", "Exists": False}


@UserRouter.get(path="/user/{username}")  # TODO: Create OpenAPI docs
def getPublicKey(username: str):
    query = users.objects(username=username)
    if query.count() == 0:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"The user {username} does not exist",
        )
    return {"detail": query[0].public_key}


# Create User
@UserRouter.post(
    path="/user",
    status_code=HTTPStatus.CREATED,
    summary="Creates a user.",
    responses={
        HTTPStatus.CONFLICT.value: {
            "description": "Occurs if a user already exists.",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User already exists. A logged in user can delete their account by a delete request to /user"
                    }
                },
            },
        },
    },
)
def createUser(user: User):
    _userLogger.info(f"Processing Create :{user.username}")
    if not Helper.validate_APIKey(key=user.api_key):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid API Key",
        )
    if usernameExists(user.username)["Exists"]:
        _userLogger.info(f"Username {user.username} already exists")
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User already exists. A logged in user can delete their account by a delete request to /user",
        )
    if not Helper.validate_password(user.password):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,  # TODO This likely should be something else
            detail="This password does not meet the minimum requirements.",
        )
    user.password = _hasher.hash(user.password)
    users.create(
        username=user.username,
        password=user.password,
        public_key=user.public_key,
        api_key=user.api_key,
    )
    return {"detail": f"Successfully created {user.username}"}


# Delete User
@UserRouter.delete(
    path="/user",
    status_code=HTTPStatus.OK,
    summary="Deletes a user.",
    responses={
        HTTPStatus.CONFLICT.value: {
            "description": "Occurs if a username does not exists.",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {"detail": "The user Alex13 does not exist"}
                },
            },
        },
    },
)
def deleteUser(user: User):
    _userLogger.info(f"Processing Delete:{user.username}")
    query = users.objects(username=user.username)
    if query.count() == 0:
        _userLogger.info(
            f"Username {user.username} does not exists to delete. Raising Exception."
        )
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"The user {user.username} does not exist or is not logged in",
        )
    _userLogger.info(f"User Exists. Checking if logged in of {user.username}")
    db_user = query[0]
    if not db_user.logged_in:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"The user {user.username} does not exist or is not logged in.",
        )
    try:
        _hasher.verify(db_user.password, user.password)
    except (VerificationError, VerifyMismatchError):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid Password or username",
        )
    users.delete(db_user)
    _userLogger.info(f"Successfully deleted {user.username}")
    return {"detail": f"Successfully deleted {user.username}"}


# Login User
@UserRouter.put(
    path="/user",
    status_code=HTTPStatus.OK,
    summary="Login a user.",
    responses={  # TODO: This needs to be completed. Copied from another
        HTTPStatus.CONFLICT.value: {
            "description": "Occurs if a username does not exists.",
            "model": Detail,
            "content": {
                "application/json": {
                    "example": {"detail": "The user Alex13 does not exist"}
                },
            },
        },
    },
)
def loginUser(request:Request,user: User):
    _userLogger.info(f"Logging in {user.username} with key {user.api_key}")
    if not Helper.validate_APIKey(user.api_key):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid API Key"
        )
    query = users.objects(username=user.username)

    if query.count() == 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid Password or username",
        )
    db_user = query[0]
    try:
        _hasher.verify(db_user.password, user.password)
    except (VerificationError, VerifyMismatchError):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid Password or username",
        )
    db_user.logged_in = request.client.host
    db_user.save()
    return {"detail": "Successful Login"}
