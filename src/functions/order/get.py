from src.utils.responses import response
from src.utils.dynamodb import orders

def handler(event, context):
    order_id = event["pathParameters"]["orderId"]

    res = orders().get_item(Key={"orderId": order_id})
    item = res.get("Item")

    if not item:
        return response(404, {"error": "Order not found"})

    return response(200, item)
