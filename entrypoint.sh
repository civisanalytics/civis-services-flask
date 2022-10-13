#!/bin/bash
# This file is fixed within the Docker image.  Do not make changes here unless you are creating a custom Docker image!

set -e

cd "${APP_DIR}"
./start_service.sh
