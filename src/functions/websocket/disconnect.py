from src.utils.dynamodb import connections

def handler(event, context):
    cid = event["requestContext"]["connectionId"]
    connections().delete_item(Key={"connectionId": cid})
    return {"statusCode": 200}
