import json
from src.utils.dynamodb import orders, gen_id, now
from src.utils.responses import response
from src.utils.eventbridge import publish

def handler(event, context):
    body = json.loads(event.get("body", "{}"))

    order_id = gen_id()
    item = {
        "orderId": order_id,
        "customerId": body.get("customerId", "demo"),
        "restaurantId": body.get("restaurantId", "REST-001"),
        "items": body.get("items", []),
        "status": "RECEIVED",
        "createdAt": now(),
    }

    orders().put_item(Item=item)

    publish(
        "order.service",
        "Order Created",
        {"orderId": order_id, "status": "RECEIVED"},
    )

    return response(201, item)
