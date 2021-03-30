# Configurability

The platform includes two separate configuration files based on YAML

* Logging
* General

## Logging

The logging configuration file contains customisation on how FastAPI will log. This file is created to be in a <a href="https://docs.python.org/3/library/logging.config.html">Python Logging Configuration</a> format.
For example, the filename of a log can be changed here, or the logging format can be customised here. A sample of a file can be seen below

```yaml
formatters:
    simple:
        format: "[%(name)s | %(levelname)s]:%(lineno)s - %(message)s"
    handlers:
        console:
            class: logging.StreamHandler
            formatter: main
            stream: ext://sys.stdout
    loggers:
        user:
            level: DEBUG
            handlers: [console]
```

## General

The general configuration controls variables upon deployment that would want to be changed. For example MongoDB's address. This file looks as follows

```yaml
MongoDB_address: "mongodb://68.241.54.139:66043/"
MongoDB_database: ilo
MongoDB_user_collection: users
MongoDB_apiKey_collection: api_keys
Potion_IP: "87.23.73.160:1642"
```

**Note** When setting the MongoDB_address, it is essential to provide the `mongodb://` prefix
