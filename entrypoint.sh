#!/bin/bash
# This file is fixed within the Docker image.  Do not make changes here unless you are creating a custom Docker image!

set -e

cd "$APP_DIR/$REPO_PATH_DIR"

if [ ! -f start_service.sh ]; then
    echo "The required file 'start_service.sh' is not found at $APP_DIR/$REPO_PATH_DIR" >&2
    exit 1
fi
./start_service.sh
