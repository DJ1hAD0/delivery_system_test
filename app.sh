#!/bin/bash

alembic upgrade head
cd /src
gunicorn src.main:app --bind=0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker