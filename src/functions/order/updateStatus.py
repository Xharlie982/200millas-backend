import json
from datetime import datetime, timezone
from src.utils.responses import response
from src.utils.db import orders
from src.utils.eventbridge import send_event


def handler(event, context):
    # 1. Obtener el orderId desde el path: /orders/{orderId}/status
    order_id = event["pathParameters"]["orderId"]

    # 2. Leer el body enviado por el cliente (nuevo estado)
    body = json.loads(event["body"])
    new_status = body.get("status")

    if not new_status:
        return response(400, {"error": "Missing 'status' field"})

    table = orders()

    # 3. Actualizar la orden en DynamoDB
    now = datetime.now(timezone.utc).isoformat()

    table.update_item(
        Key={"orderId": order_id},
        UpdateExpression="SET #s = :s, updatedAt = :u",
        ExpressionAttributeNames={
            "#s": "status"
        },
        ExpressionAttributeValues={
            ":s": new_status,
            ":u": now
        }
    )

    # 4. Publicar evento en EventBridge
    send_event(
        source="order.service",
        detail_type="Order Status Changed",
        detail={
            "orderId": order_id,
            "status": new_status,
            "updatedAt": now
        }
    )

    # 5. Respuesta JSON estándar
    return response(200, {
        "message": "Order status updated",
        "orderId": order_id,
        "status": new_status
    })
