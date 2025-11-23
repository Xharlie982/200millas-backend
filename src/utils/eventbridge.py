import os
import json
import boto3

events = boto3.client("events")

def publish(source, detail_type, detail):
    events.put_events(
        Entries=[{
            "Source": source,
            "DetailType": detail_type,
            "Detail": json.dumps(detail),
            "EventBusName": os.environ["EVENT_BUS_NAME"],
        }]
    )
