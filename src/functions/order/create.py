from decimal import Decimal
import json
import os
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
events = boto3.client("events")

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

def send_event(detail):
    events.put_events(
        Entries=[
            {
                "Source": "order.service",
                "DetailType": "Order Created",
                "Detail": json.dumps(detail),
                "EventBusName": os.environ["EVENT_BUS_NAME"]
            }
        ]
    )

def handler(event, context):
    table = dynamodb.Table(os.environ['ORDERS_TABLE'])
    body = json.loads(event['body'])

    # Generar ID
    order_id = str(uuid.uuid4())
    body["orderId"] = order_id
    body["status"] = "CREATED"

    item = decimalize(body)

    # Guardar en DynamoDB
    table.put_item(Item=item)

    # Enviar evento a EventBridge
    send_event({
        "orderId": order_id,
        "customerId": body.get("customerId"),
        "restaurantId": body.get("restaurantId"),
        "status": "CREATED"
    })

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Order created",
            "orderId": order_id
        })
    }
