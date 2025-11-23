from decimal import Decimal
import json
import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def decimalize(obj):
    """Recursively convert floats to Decimal"""
    if isinstance(obj, list):
        return [decimalize(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: decimalize(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj

def handler(event, context):
    table = dynamodb.Table(os.environ['ORDERS_TABLE'])

    body = json.loads(event['body'])

    # Agregar un ID de orden
    body["orderId"] = str(uuid.uuid4())
    body["status"] = "CREATED"

    # Convertir floats → Decimal
    item = decimalize(body)

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Order created",
            "orderId": body["orderId"]
        })
    }
