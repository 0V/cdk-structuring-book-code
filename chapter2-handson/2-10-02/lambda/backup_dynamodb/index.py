import json
import boto3
from datetime import datetime, timezone
import urllib3

dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
http = urllib3.PoolManager()

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def send_response(event, context, response_status, response_data):
    """CloudFormationにレスポンスを送信"""
    response_body = json.dumps({
        "Status": response_status,
        "Reason": f"See CloudWatch Log Stream: {context.log_stream_name}",
        # Updateで異なるPhysicalResourceIdを返すとリソース置換と解釈され、
        # 旧IDに対するDeleteが後続で発行される。呼び出しごとに変わる
        # log_stream_nameは使わず、Stack内で一意な論理IDを使う
        "PhysicalResourceId": event.get("PhysicalResourceId") or event["LogicalResourceId"],
        "StackId": event["StackId"],
        "RequestId": event["RequestId"],
        "LogicalResourceId": event["LogicalResourceId"],
        "Data": response_data,
    })
    try:
        http.request("PUT", event["ResponseURL"],
                     body=response_body.encode("utf-8"),
                     headers={"Content-Type": "application/json"})
        print("Response sent successfully")
    except Exception as e:
        print(f"Failed to send response: {str(e)}")


def backup_table_to_s3(table_name, bucket_name):
    """DynamoDBテーブルのデータをS3にバックアップ"""
    items = []
    response = dynamodb.scan(TableName=table_name)
    items.extend(response.get("Items", []))

    # ページネーション処理
    while "LastEvaluatedKey" in response:
        response = dynamodb.scan(TableName=table_name,
                                 ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response.get("Items", []))

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_key = f"backups/{table_name}/{timestamp}/data.json"
    backup_data = {"table_name": table_name, "timestamp": timestamp, "items": items}

    s3.put_object(Bucket=bucket_name, Key=backup_key,
                  Body=json.dumps(backup_data, indent=2),
                  ContentType="application/json")

    print(f"Backup completed: s3://{bucket_name}/{backup_key}")
    return {"BackupLocation": f"s3://{bucket_name}/{backup_key}", "ItemCount": len(items)}


def handler(event, context):
    """カスタムリソースのハンドラー"""
    # イベントの読み取りもtryの中に入れる。ここで例外が出ると
    # CloudFormationへ応答を返せず、Stackが1時間待ち続ける
    try:
        print(f"Received event: {json.dumps(event)}")
        request_type = event["RequestType"]
        table_name = event["ResourceProperties"]["TableName"]
        bucket_name = event["ResourceProperties"]["BucketName"]

        if request_type == "Delete":
            print(f"DELETE: Backing up table {table_name} to {bucket_name}")
            try:
                backup_result = backup_table_to_s3(table_name, bucket_name)
                send_response(event, context, SUCCESS, {"BackupDetails": backup_result})
            except Exception as e:
                # DeleteでFAILEDを返すとStackがDELETE_FAILEDになり削除できなくなる。
                # 失敗はログに残し、Stackの削除自体は進められるようにする
                print(f"Backup failed on delete: {str(e)}")
                send_response(event, context, SUCCESS, {"Message": f"Backup failed: {str(e)}"})
        else:
            print(f"{request_type}: No action required")
            send_response(event, context, SUCCESS, {"Message": f"{request_type} completed"})
    except Exception as e:
        print(f"Error: {str(e)}")
        send_response(event, context, FAILED, {"Message": str(e)})
