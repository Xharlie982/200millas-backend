import json
from datetime import datetime, timezone
from src.utils.db import orders
from src.utils.responses import response

def handler(event, context):
    order_id = event["orderId"]
    table = orders()

    table.update_item(
        Key={"orderId": order_id},
        UpdateExpression="SET workflowStartedAt = :t",
        ExpressionAttributeValues={
            ":t": datetime.now(timezone.utc).isoformat()
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Workflow updated"})
    }
