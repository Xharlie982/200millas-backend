from src.utils.responses import response
from src.utils.dynamodb import orders

def handler(event, context):
    res = orders().scan()
    return response(200, res.get("Items", []))
