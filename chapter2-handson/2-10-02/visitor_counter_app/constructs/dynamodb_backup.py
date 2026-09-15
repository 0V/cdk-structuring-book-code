from aws_cdk import Duration, CustomResource, aws_lambda as lambda_, aws_iam as iam
from constructs import Construct


class DynamoDBBackupConstruct(Construct):
    """DynamoDBテーブルのバックアップカスタムリソース"""

    def __init__(self, scope, construct_id, table_name, table_arn, bucket_name, bucket_arn, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # カスタムリソース用のLambda関数
        backup_lambda = lambda_.Function(self, "BackupFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda/backup_dynamodb"),
            timeout=Duration.minutes(5),
            memory_size=512,
        )

        # DynamoDBテーブルへの読み取り権限
        backup_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["dynamodb:Scan", "dynamodb:DescribeTable"],
            resources=[table_arn],
        ))

        # S3バケットへの書き込み権限
        backup_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:PutObject", "s3:PutObjectAcl"],
            resources=[f"{bucket_arn}/*"],
        ))

        # カスタムリソース
        # Lambda関数がResponseURLへ直接応答する実装のため、Lambda関数のARNを
        # service_tokenに指定する（応答処理を代行するcustom_resources.Providerは使わない）
        self.custom_resource = CustomResource(self, "BackupCustomResource",
            service_token=backup_lambda.function_arn,
            properties={"TableName": table_name, "BucketName": bucket_name},
        )
