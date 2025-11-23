import os
import boto3
from datetime import datetime, timezone
import uuid

dynamodb = boto3.resource("dynamodb")

def orders():
    return dynamodb.Table(os.environ["ORDERS_TABLE"])

def connections():
    return dynamodb.Table(os.environ["CONNECTIONS_TABLE"])

def now():
    return datetime.now(timezone.utc).isoformat()

def gen_id():
    return f"ORD-{uuid.uuid4().hex[:8].upper()}"
