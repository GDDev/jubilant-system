#!/bin/sh

CONFIG_FILE=".settings.cfg"

SECRET_KEY=$(python -c 'import secrets; print(str(secrets.token_hex()))')

echo "SECRET_KEY = \"$SECRET_KEY\"" > "$CONFIG_FILE"

export FLASK_CONFIG_PATH="$(pwd)/$CONFIG_FILE"