import boto3
import os
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ORDERS_TABLE"])

def handler(event, context):
    """
    Marca la orden como READY.

    Compatible con:
    1) Step Functions (event.detail.orderId)
    2) API Gateway manual (pathParameters.orderId)
    """

    order_id = None

    # ---- CASE 1: Triggered by Step Functions ----
    if "detail" in event:
        order_id = event["detail"].get("orderId")

    # ---- CASE 2: Triggered manually via HTTP call ----
    elif "pathParameters" in event:
        order_id = event["pathParameters"].get("orderId")

    else:
        raise Exception(f"Unsupported event format: {event}")

    if not order_id:
        raise Exception(f"Invalid event, orderId not found. Event received: {event}")

    table.update_item(
        Key={"orderId": order_id},
        UpdateExpression="SET #st = :ready",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={":ready": "READY"}
    )

    return {
        "orderId": order_id,
        "newStatus": "READY",
        "message": "Order marked READY"
    }
