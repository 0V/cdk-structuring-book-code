from aws_cdk import (
    Stack, RemovalPolicy, Duration,
    aws_s3 as s3, aws_lambda as lambda_, aws_dynamodb as dynamodb,
    aws_events as events, aws_events_targets as targets,
)
from constructs import Construct


class ReportStack(Stack):
    """レポート生成Stack（クロスStack参照パターン）"""

    def __init__(self, scope: Construct, construct_id: str, visits_table: dynamodb.ITable, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.report_bucket = s3.Bucket(self, "ReportBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        self.generate_report_lambda = lambda_.Function(self, "GenerateReportFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda/generate_report"),
            environment={"TABLE_NAME": visits_table.table_name, "BUCKET_NAME": self.report_bucket.bucket_name},
            timeout=Duration.seconds(30),
        )

        # テーブルのオブジェクトを受け取っているため、権限付与もこのStack内で完結する
        visits_table.grant_read_data(self.generate_report_lambda)

        self.report_bucket.grant_write(self.generate_report_lambda)

        # EventBridgeルールの作成（毎日午前0時に実行）
        rule = events.Rule(self, "DailyReportRule",
            schedule=events.Schedule.cron(hour="0", minute="0"),
            description="Generate daily visitor report",
        )
        rule.add_target(targets.LambdaFunction(self.generate_report_lambda))
