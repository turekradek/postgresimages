#!/bin/bash

# Start PostgreSQL server in the background
/usr/local/bin/docker-entrypoint.sh postgres &

# Wait for PostgreSQL to start
sleep 5

# Run the Python application
python3 app.py
