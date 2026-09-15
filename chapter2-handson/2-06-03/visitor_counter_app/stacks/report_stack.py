from aws_cdk import (
    Stack, RemovalPolicy, Duration, Fn,
    aws_s3 as s3, aws_lambda as lambda_, aws_iam as iam,
    aws_events as events, aws_events_targets as targets,
)
from constructs import Construct


class ReportStack(Stack):
    """レポート生成Stack（Fn::ImportValue/Exportパターン）"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # エクスポートされた値をインポート
        table_name = Fn.import_value("VisitorCounter-TableName")
        table_arn = Fn.import_value("VisitorCounter-TableArn")

        # S3バケットの作成（レポート保存用）
        self.report_bucket = s3.Bucket(self, "ReportBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Lambda関数の作成（レポート生成用）
        self.generate_report_lambda = lambda_.Function(self, "GenerateReportFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda/generate_report"),
            environment={"TABLE_NAME": table_name, "BUCKET_NAME": self.report_bucket.bucket_name},
            timeout=Duration.seconds(30),
        )

        # DynamoDBへの読み取り権限を付与（ARNを使用）
        self.generate_report_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["dynamodb:Scan", "dynamodb:Query", "dynamodb:GetItem"],
                resources=[table_arn],
            )
        )

        self.report_bucket.grant_write(self.generate_report_lambda)

        # EventBridgeルールの作成（毎日午前0時に実行）
        rule = events.Rule(self, "DailyReportRule",
            schedule=events.Schedule.cron(hour="0", minute="0"),
            description="Generate daily visitor report",
        )
        rule.add_target(targets.LambdaFunction(self.generate_report_lambda))
