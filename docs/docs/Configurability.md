# Configurability

The platform includes two separate configuration files based on YAML

* Logging
* General

## Logging

The logging configuration file contains customisation on how FastAPI will log. This file is created to be in a <a href="https://docs.python.org/3/library/logging.config.html">Python Logging Configuration</a> format.
For example, the filename of a log can be changed here, or the logging format can be customised here. A sample of a file can be seen below.

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

The general configuration controls variables upon deployment that are desirable to be changed without code changes. For example, Cassandra's address. This file looks as follows.

```yaml
Cassandra_address: "127.0.0.1"
Cassandra_keyspace: "ilo"
Potion_IP: "0.0.0.0:4000"
```

!!! note
    The Cassandra keyspace must be created; Ilo will not make it. A keyspace can be created with the following command within the CQL shell
    ```SQL
    CREATE keyspace ilo WITH replication={'class':'SimpleStrategy','replication_factor':3};
    ```
    The tables used by Ilo will be created automatically.