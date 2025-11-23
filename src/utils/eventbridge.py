import os
import json
import boto3

events = boto3.client("events")
bus_name = os.environ["EVENT_BUS_NAME"]

def send_event(source, detail_type, detail):
    events.put_events(
        Entries=[
            {
                "Source": source,
                "DetailType": detail_type,
                "Detail": json.dumps(detail),
                "EventBusName": bus_name
            }
        ]
    )
