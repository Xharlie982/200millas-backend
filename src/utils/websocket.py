import os
import json
import boto3
from .dynamodb import connections

_client = None

def _client():
    global _client
    if _client:
        return _client

    endpoint = os.environ["WEBSOCKET_ENDPOINT"].replace("wss://", "https://")
    _client = boto3.client("apigatewaymanagementapi", endpoint_url=endpoint)
    return _client

def broadcast(payload):
    table = connections()
    scan = table.scan()

    for item in scan.get("Items", []):
        cid = item["connectionId"]
        try:
            _client().post_to_connection(
                ConnectionId=cid,
                Data=json.dumps(payload).encode("utf-8"),
            )
        except Exception:
            table.delete_item(Key={"connectionId": cid})
