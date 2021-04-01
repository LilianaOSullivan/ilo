#!/bin/bash
uvicorn app:app --ssl-keyfile localhost.key --ssl-certfile localhost.crt --port 7999
