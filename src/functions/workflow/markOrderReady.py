import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["ORDERS_TABLE"])

def handler(event, context):
    """
    Marca la orden como READY al terminar el workflow.
    """

    # Step Functions recibe el evento de EventBridge con esta forma:
    # {
    #   "version": "0",
    #   "id": "...",
    #   "detail-type": "Order Created",
    #   "source": "order.service",
    #   "detail": {
    #       "orderId": "...",
    #       "customerId": "...",
    #       ...
    #   }
    # }
    
    detail = event["detail"]
    order_id = detail["orderId"]
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
        "newStatus": "READY"
    }
