#!/bin/bash
# This file is launched by entrypoint.sh to start your application.  Install any additional dependencies here or in requirements.txt.

set -e

echo "Installing dependencies"
pip install -r requirements.txt

gunicorn -b 0.0.0.0:${CIVIS_SERVICE_PORT:-3838} -w 4 "civis_app:create_app()" --timeout 2000
