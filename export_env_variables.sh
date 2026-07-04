#!/bin/bash

echo "To have the environment variable persist in the current terminal session, it should be run like this:"
echo ". export_env_variables.sh"

echo "Exporting environment varibles from the 'email.env' file"
export $(xargs < email.env)
