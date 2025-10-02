#!/bin/bash

echo "start create DB"

python3 init_db.py

echo "DB created"

exec gunicorn app:app
