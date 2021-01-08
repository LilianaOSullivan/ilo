import logging
import logging.config
from typing import Dict
import pymongo

import yaml
from fastapi import FastAPI
import Config

import Helper


def startup():
    import resource

    ## Seems to fix issues with either MongoDB or FastAPI. Too many open files error 24.
    ## https://stackoverflow.com/questions/2569620/socket-accept-error-24-to-many-open-files
    resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

    with open("logging_config.yaml", "r") as y:
        logging.config.dictConfig(yaml.safe_load(y.read()))

    _generalLogger = logging.getLogger("general")
    _generalLogger.info("Starting ilo..Parsing general config")
    config: Dict = {}
    with open("general_config.yaml", "r") as y:
        config = yaml.safe_load(y.read())
    for k, v in config.items():
        setattr(Config, k, v)
    del config
    _generalLogger.info("Creating Helper")
    Helper.logger = _generalLogger
    Helper.keyDB = pymongo.MongoClient(Config.MongoDB_address)[Config.MongoDB_database][
        Config.MongoDB_apiKey_collection
    ]
    _generalLogger.info("Starting FastAPI")


startup()

tags_metadata = [
    {
        "name": "Users",
        "description": "All Operations with users profiles.",
    },
    {
        "name": "API Keys",
        "description": "Manage API Keys. Enables the generation and deletion of keys.",
    },
    {
        "name": "Test Client",
        "description": "A test client showcasing API usage from a browser",
    },
]
app = FastAPI(
    title="Ilo",
    description="A 4th year software development project to create an API that enables secure communication between multiple of its users.",
    version="In Development",
    openapi_tags=tags_metadata,
)

from routers.ApiKey import ApiKeyRouter
from routers.TestClient import TestClient
from routers.Potion import potionRouter
from routers.User import UserRouter

app.include_router(UserRouter)
app.include_router(ApiKeyRouter)
app.include_router(TestClient)
#app.include_router(potionRouter)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# TODO: Use Aync Mongo? Probably not worth as transitioning to Cassandra, that supports Async
# TODO: Apply validations of API Key
# TODO: Connect to potion
# TODO: Fix posting models. Eg User model being reused
# TODO: Cryptography
# TODO: Does user input need to be escaped for MongoDB if not processing on the data?

# QUESTION: secrets.compare_digest() when logging in dont support unicode/non-ASCII characters :(
# https://github.com/python/cpython/blob/32bd68c839adb7b42af12366ab0892303115d1d1/Modules/_hashopenssl.c#L1894
# Using .encode() to convert to bytes and then compare. This is a weird result, opinions?
# Assuming b-string dosent specify encoding type? Or defaults to ASCII?

"""
>>> import secrets
>>> s ="💕"
>>> s
'💕'
>>> secrets.compare_digest(s,"d")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: comparing strings with non-ASCII characters is not supported
>>> secrets.compare_digest(s.encode('utf-8'),b"d")
False
>>> secrets.compare_digest(s.encode('utf-8'),b"💕")
  File "<stdin>", line 1
    secrets.compare_digest(s.encode('utf-8'),b"💕")
                                                 ^
SyntaxError: bytes can only contain ASCII literal characters.
>>> secrets.compare_digest(s.encode('utf-8'),"💕".encode('utf-8'))
True
>>> "💕".encode('utf-8')
b'\xf0\x9f\x92\x95'
>>> type("💕".encode('utf-8'))
<class 'bytes'>
>>> 
"""
