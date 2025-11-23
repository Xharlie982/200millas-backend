import os
import boto3

ddb = boto3.resource("dynamodb")
connections_table = ddb.Table(os.environ["CONNECTIONS_TABLE"])

def handler(event, context):
    connection_id = event["requestContext"]["connectionId"]

    connections_table.put_item(Item={
        "connectionId": connection_id
    })

    return {
        "statusCode": 200,
        "body": "connected"
    }
