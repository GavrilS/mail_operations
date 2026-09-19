#!/bin/bash


if [[ ! -d ./env ]]; then
    echo "Environment is missing so setting it up now"
    python3 -m venv env/
fi

echo "Installing python dependencies"

source env/bin/activate

python3 -m pip install -r requirements.txt --upgrade

deactivate
