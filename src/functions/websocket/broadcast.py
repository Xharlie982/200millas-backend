from src.utils.websocket import broadcast

def handler(event, context):
    # El evento de EventBridge llega así:
    # {
    #   "detail-type": "Order Status Changed",
    #   "source": "order.service",
    #   "detail": {
    #       "orderId": "...",
    #       "status": "PREPARING"
    #   }
    # }

    detail = event["detail"]

    broadcast({
        "type": "ORDER_UPDATED",
        "data": detail
    })

    return {"statusCode": 200}
