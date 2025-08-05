#!/bin/bash

TIBBER_TOKEN=$(grep '^tibber_token:' secrets.yaml | awk '{print $2}')
INFLUX_URL=$(grep '^influx_url:' secrets.yaml | awk '{print $2}')
INFLUXDB_TOKEN=$(grep '^influxdb_token:' secrets.yaml | awk '{print $2}')
INFLUXDB_ORGANIZATION=$(grep '^influxdb_organization:' secrets.yaml | awk '{print $2}')
INFLUXDB_BUCKET=$(grep '^influxdb_bucket:' secrets.yaml | awk '{print $2}')

export TIBBER_TOKEN
export INFLUX_URL
export INFLUXDB_TOKEN
export INFLUXDB_ORGANIZATION
export INFLUXDB_BUCKET

. ~/venvs/tibberenv/bin/activate
python fetch_energy_usage.py

