from src.utils.dynamodb import connections

def handler(event, context):
    cid = event["requestContext"]["connectionId"]
    connections().put_item(Item={"connectionId": cid})
    return {"statusCode": 200}
