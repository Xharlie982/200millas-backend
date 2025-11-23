def handler(event, context):
    """
    Este estado simplemente confirma que la orden es válida.
    No necesita leer DB ni nada.
    """
    order_id = event["detail"]["orderId"]

    return {
        "orderId": order_id,
        "validated": True
    }
