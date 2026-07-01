#!/bin/bash

echo "Exporting environment varibles from the 'email.env' file"
export $(xargs < email.env)

printenv
