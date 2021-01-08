import logging
import time
from http import HTTPStatus

import Config
import Helper
import pymongo
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from fastapi import APIRouter, HTTPException
from models import Detail, User
from pymongo.collection import Collection

UserRouter: APIRouter = APIRouter(tags=["Users"])

_hasher = PasswordHasher()
_userLogger: logging.Logger = logging.getLogger("user")
_userLogger.info(
    f"Connecting to userDB: {Config.MongoDB_address}/{Config.MongoDB_database}/{Config.MongoDB_user_collection}"
)
userDB: Collection = pymongo.MongoClient(Config.MongoDB_address)[
    Config.MongoDB_database
][Config.MongoDB_user_collection]
_userLogger.info("Connected to userDB")


@UserRouter.options(path="/user/{username}")  # TODO: Create OpenAPI docs
def usernameExists(username: str):
    if userDB.find_one({"username": username}) is not None:
        return {"detail": "Username Exists", "Exists": True}
    return {"detail": "Username dosent exist", "Exists": False}


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
    _userLogger.info(f"Procesing Create :{user.username}")
    if not Helper.validate_APIKey(user.apiKey):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid API Key",
        )
    if userDB.find_one({"username": user.username}) is not None:
        _userLogger.info(f"Username {user.username} already exists")
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User already exists. A logged in user can delete their account by a delete request to /user",
        )

    user.password = _hasher.hash(user.password)
    userDB.insert_one(vars(user))
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
    query = userDB.find_one({"username": user.username})
    if query is None:
        _userLogger.info(
            f"Username {user.username} does not exists to delete. Raising Exception."
        )
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"The user {user.username} does not exist",
        )
    _userLogger.info(f"User Exists. Deleting {user.username}")
    userDB.delete_one(query)
    _userLogger.info(f"Successfully deleted {user.username}")
    return {"detail": f"Successfully deleted {user.username}"}


# Login User
@UserRouter.put(
    path="/user",
    status_code=HTTPStatus.OK,
    summary="Login a user.",
    responses={  # BUG: This needs to be completed. Copied from another
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
def loginUser(user: User):
    _userLogger.info(f"Logging in {user.username} with key {user.apiKey}")
    if not Helper.validate_APIKey(user.apiKey):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid API Key"
        )
    result = userDB.find_one({"username": user.username})

    if result is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid Password or username",
        )

    try:
        _hasher.verify(result["password"], user.password)
    except (VerificationError, VerifyMismatchError) as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Invalid Password or username",
        )
    # TODO: Below is unused, and maybe should be in API key users=[]
    result["last_login"] = time.time()
    # TODO: Below unused, and not timing out the user
    result["loggin_in"] = True

    return {"detail": "Successful Login"}
