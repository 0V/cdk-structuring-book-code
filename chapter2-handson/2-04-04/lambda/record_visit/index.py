import json
import os
import uuid
from datetime import datetime, timezone
import boto3

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["TABLE_NAME"]
table = dynamodb.Table(table_name)


def handler(event, context):
    """訪問を記録するLambda関数"""
    try:
        body = {}
        if event.get("body"):
            body = json.loads(event["body"])

        visit_id = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()

        item = {
            "id": visit_id,
            "timestamp": timestamp,
            "page": body.get("page", "/"),
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"visit_id": visit_id}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
