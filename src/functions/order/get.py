import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ORDERS_TABLE'])

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

def handler(event, context):
    orderId = event["pathParameters"]["orderId"]

    resp = table.get_item(Key={"orderId": orderId})

    if "Item" not in resp:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Order not found"})
        }

    item = convert_decimal(resp["Item"])

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }
