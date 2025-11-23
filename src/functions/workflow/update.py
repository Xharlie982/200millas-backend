import json
from datetime import datetime, timezone
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ORDERS_TABLE"])

def handler(event, context):
    detail = event["detail"]
    order_id = detail["orderId"]

    table.update_item(
        Key={"orderId": order_id},
        UpdateExpression="SET workflowStartedAt = :t",
        ExpressionAttributeValues={
            ":t": datetime.now(timezone.utc).isoformat()
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "workflow updated"})
    }
