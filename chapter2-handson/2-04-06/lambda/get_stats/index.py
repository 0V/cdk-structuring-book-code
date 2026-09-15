import json
import os
from datetime import datetime, timedelta, timezone
from collections import Counter
import boto3

dynamodb = boto3.resource("dynamodb")
table_name = os.environ["TABLE_NAME"]
table = dynamodb.Table(table_name)


def handler(event, context):
    """訪問統計を取得するLambda関数"""
    try:
        query_params = event.get("queryStringParameters") or {}
        days = int(query_params.get("days", 7))
        start_date = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

        response = table.scan()
        items = response.get("Items", [])

        filtered_items = [
            item for item in items if item.get("timestamp", "") >= start_date
        ]

        total_visits = len(filtered_items)
        page_counts = Counter(item.get("page", "/") for item in filtered_items)

        stats = {
            "period_days": days,
            "total_visits": total_visits,
            "top_pages": [
                {"page": page, "count": count}
                for page, count in page_counts.most_common(10)
            ],
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(stats),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
