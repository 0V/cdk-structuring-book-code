from aws_cdk import Stack, RemovalPolicy, aws_s3 as s3, aws_ssm as ssm
from constructs import Construct
from visitor_counter_app.constructs.visitor_counter import VisitorCounterConstruct
from visitor_counter_app.constructs.dynamodb_backup import DynamoDBBackupConstruct


class VisitorCounterStack(Stack):
    """訪問者カウンターStack（カスタムリソース付き）"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.visitor_counter = VisitorCounterConstruct(self, "VisitorCounter")

        # バックアップ用S3バケットの作成
        backup_bucket = s3.Bucket(self, "BackupBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.RETAIN,
        )

        # DynamoDBバックアップカスタムリソース
        DynamoDBBackupConstruct(self, "DynamoDBBackup",
            table_name=self.visitor_counter.table.table_name,
            table_arn=self.visitor_counter.table.table_arn,
            bucket_name=backup_bucket.bucket_name,
            bucket_arn=backup_bucket.bucket_arn,
        )

        self.table = self.visitor_counter.table
        self.backup_bucket = backup_bucket

        # SSMパラメータの登録は引き続き必要（ReportStackが参照している）
        ssm.StringParameter(self, "TableNameParameter",
            parameter_name="/visitor-counter/table-name",
            string_value=self.table.table_name,
            description="DynamoDB table name for visitor counter",
        )

        ssm.StringParameter(self, "TableArnParameter",
            parameter_name="/visitor-counter/table-arn",
            string_value=self.table.table_arn,
            description="DynamoDB table ARN for visitor counter",
        )
