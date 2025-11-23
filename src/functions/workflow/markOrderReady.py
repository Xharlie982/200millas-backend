import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ORDERS_TABLE"])

def handler(event, context):
    """
    Marca la orden como READY al terminar el workflow.
    """
    order_id = event.get("orderId")

    table.update_item(
        Key={"orderId": order_id},
        UpdateExpression="SET #st = :ready",
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={":ready": "READY"}
    )

    return {
        "orderId": order_id,
        "newStatus": "READY"
    }
