import logging
import logging.config
from typing import Dict

import pymongo
import yaml
from fastapi import FastAPI

from Config import Config
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
        setattr(Config, k.strip(), v.strip())
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
from routers.Potion import potionRouter
from routers.TestClient import TestClient
from routers.User import UserRouter

app.include_router(UserRouter)
app.include_router(ApiKeyRouter)
app.include_router(TestClient)
app.include_router(potionRouter)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
