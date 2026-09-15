import json
import os
from datetime import datetime, timedelta, timezone
from collections import Counter
import boto3

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
table_name = os.environ["TABLE_NAME"]
bucket_name = os.environ["BUCKET_NAME"]
table = dynamodb.Table(table_name)


def handler(event, context):
    """訪問統計レポートを生成してS3に保存するLambda関数"""
    try:
        start_date = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        response = table.scan()
        items = response.get("Items", [])
        filtered_items = [item for item in items if item.get("timestamp", "") >= start_date]

        total_visits = len(filtered_items)
        page_counts = Counter(item.get("page", "/") for item in filtered_items)

        report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": {"total_visits": total_visits},
            "top_pages": [{"page": p, "count": c} for p, c in page_counts.most_common(10)],
        }

        report_key = f"reports/{datetime.now(timezone.utc).strftime('%Y/%m/%d')}/report.json"
        s3.put_object(Bucket=bucket_name, Key=report_key, Body=json.dumps(report, indent=2))

        return {"statusCode": 200, "body": json.dumps({"message": "Report generated"})}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
