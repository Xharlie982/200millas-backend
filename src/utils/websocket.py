import os
import json
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key

ddb = boto3.resource("dynamodb")
apigw = boto3.client("apigatewaymanagementapi", endpoint_url=os.environ["WEBSOCKET_ENDPOINT"])
connections_table = ddb.Table(os.environ["CONNECTIONS_TABLE"])


def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj


def get_all_connections():
    res = connections_table.scan()
    return res.get("Items", [])


def send_to_connection(connection_id, payload):
    try:
        apigw.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(payload).encode("utf-8")
        )
    except apigw.exceptions.GoneException:
        # limpiar conexiones muertas
        connections_table.delete_item(Key={"connectionId": connection_id})


def broadcast(payload):
    payload = convert_decimal(payload)
    connections = get_all_connections()

    for conn in connections:
        send_to_connection(conn["connectionId"], payload)
