#!/bin/sh

cd ./app
uvicorn main:app --reload --host "192.168.0.105" --port 5000 --reload
