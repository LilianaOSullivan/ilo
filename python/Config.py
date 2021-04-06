from typing import Final


class Config:
    MongoDB_address:str = "mongodb://127.0.0.1:27017/"
    MongoDB_database:str = "ilo"
    MongoDB_user_collection:str = "users"
    MongoDB_apiKey_collection:str = "api_keys"
    Potion_IP:str = "0.0.0.0:4000"

    LOGGING_CONFIG_DEFAULT:Final = """version: 1
formatters:
    simple:
        format: "[%(name)s | %(levelname)s]:%(lineno)s - %(message)s"
    main:
        format: "[%(asctime)s]{%(name)s | %(levelname)s}:%(lineno)s - %(message)s"
handlers:
    console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: main
        stream: ext://sys.stdout
    users:
        class: logging.handlers.RotatingFileHandler
        formatter: main
        filename: user.log
    general:
        class: logging.handlers.RotatingFileHandler
        formatter: main
        filename: general.log
    api:
        class: logging.handlers.RotatingFileHandler
        formatter: main
        filename: api.log
loggers:
    user:
        level: DEBUG
        handlers: [users]
    general:
        level: DEBUG
        handlers: [general]
    api:
        level: DEBUG
        handlers: [api]"""

    GENERAL_CONFIG_DEFAULT:Final = """MongoDB_address: "mongodb://127.0.0.1:27017/"
MongoDB_database: ilo
MongoDB_user_collection: users
MongoDB_apiKey_collection: api_keys
Potion_IP: "0.0.0.0:4000"
"""