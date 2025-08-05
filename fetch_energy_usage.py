#!/usr/bin/python

import os
import requests
import json
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

tibber_token = os.getenv("TIBBER_TOKEN").strip("'")
influx_url = os.getenv("INFLUX_URL").strip("'")
influxdb_token = os.getenv("INFLUXDB_TOKEN").strip("'")
influxdb_organization = os.getenv("INFLUXDB_ORGANIZATION").strip("'")
influxdb_bucket  = os.getenv("INFLUXDB_BUCKET").strip("'")

QUERY = """
{
  viewer {
    homes {
      consumption(resolution: DAILY, last: 365) {
        nodes {
          from
          consumption
          unitPrice
          cost
        }
      }
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {tibber_token}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.tibber.com/v1-beta/gql",
    json={"query": QUERY},
    headers=headers
)

data = response.json()

try:
    nodes = data["data"]["viewer"]["homes"][0]["consumption"]["nodes"]
    print(f"Retrieved {len(nodes)} days of data.")

except (KeyError, IndexError):
    print("Error: Could not find consumption data.")
    exit(1)

records = [
    {
        "measurement": "electricity_usage",
        "time": node["from"],
        "fields": {
            "consumption_kWh": node["consumption"],
            "price_SEK_per_kWh": node["unitPrice"],
            "cost_SEK": node["cost"]
        }
    }
    for node in nodes if node["consumption"] is not None
]

with InfluxDBClient(url=influx_url, token=influxdb_token, org=influxdb_organization) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=influxdb_bucket,
                    org=influxdb_organization,
                    record=records,
                    write_precision=WritePrecision.S)

