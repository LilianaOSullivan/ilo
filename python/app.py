import logging
import logging.config
import os
import sys
from typing import Dict

import yaml
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI

import Helper
from CassandraModels import *
from Config import Config


def startup():

    import resource

    ## Fixes the issue "Too many open files error 24"
    ## https://stackoverflow.com/questions/2569620/socket-accept-error-24-to-many-open-files
    resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

    if not os.path.exists("logging_config.yaml"):
        with open("logging_config.yaml", "w") as f:
            f.write(Config.LOGGING_CONFIG_DEFAULT)
            print("Created logging_config.yaml. Using default settings...")
            logging.config.dictConfig(yaml.safe_load(Config.LOGGING_CONFIG_DEFAULT))
    else:
        try:
            with open("logging_config.yaml", "r") as y:
                logging.config.dictConfig(yaml.safe_load(y.read()))
        except:
            print("Error Parsing logging_config. Using default Ilo configuration")
            logging.config.dictConfig(yaml.safe_load(Config.LOGGING_CONFIG_DEFAULT))

    _generalLogger = logging.getLogger("general")
    _generalLogger.info("Starting ilo...Parsing general config")
    if not os.path.exists("general_config.yaml"):
        with open("general_config.yaml", "w") as f:
            f.write(Config.GENERAL_CONFIG_DEFAULT)
            print("Created general_config.yaml. Using default settings...")
            _generalLogger.info(
                "Created general_config.yaml. Using default settings..."
            )
    else:
        config: Dict = {}
        try:
            with open("general_config.yaml", "r") as y:
                config = yaml.safe_load(y.read())
        except:
            print("Error parsing general_config. Using default Ilo configuration")
            config = yaml.safe_load(Config.GENERAL_CONFIG_DEFAULT)
        for k, v in config.items():
            k, v = k.strip(), v.strip()
            if len(k) != 0 and len(v) != 0:
                setattr(Config, k, v)
        del config
    _generalLogger.info("Creating Helper")
    Helper.logger = _generalLogger
    _generalLogger.info("Connecting to Cassandra")
    try:
        connection.setup(
            [Config.Cassandra_address], Config.Cassandra_keyspace, protocol_version=3
        )
        sync_table(users, [Config.Cassandra_keyspace])
        sync_table(api_keys, [Config.Cassandra_keyspace])
    except Exception as e:
        _generalLogger.critical(
            "Failed to connect to Cassandra with the following exception"
        )
        _generalLogger.exception(e)
        print(e)
        sys.exit(1)
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
