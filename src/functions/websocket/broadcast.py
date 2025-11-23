from src.utils.websocket import broadcast

def handler(event, context):
    detail = event.get("detail", {})
    broadcast({
        "type": "order_update",
        "detail": detail
    })
    return {}
