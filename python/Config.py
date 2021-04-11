from typing import Final


class Config:
    Cassandra_address: str = "127.0.0.1"
    Cassandra_keyspace: str = "ilo"
    Potion_IP: str = "0.0.0.0:4000"

    LOGGING_CONFIG_DEFAULT: Final = """version: 1
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

    GENERAL_CONFIG_DEFAULT: Final = """Cassandra_address: "127.0.0.1"
Cassandra_keyspace: "ilo"
Potion_IP: "0.0.0.0:4000"
"""