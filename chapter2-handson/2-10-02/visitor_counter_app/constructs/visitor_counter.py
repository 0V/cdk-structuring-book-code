from aws_cdk import (
    RemovalPolicy,
    Duration,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
from constructs import Construct


class VisitorCounterConstruct(Construct):
    """訪問者カウンターのConstruct（L2 Construct版 - 推奨）"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDBテーブル
        self.table = dynamodb.Table(
            self,
            "VisitsTable",
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # 訪問記録用Lambda
        self.record_visit_lambda = lambda_.Function(
            self,
            "RecordVisitFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda/record_visit"),
            environment={"TABLE_NAME": self.table.table_name},
            timeout=Duration.seconds(10),
        )

        # 統計取得用Lambda
        self.get_stats_lambda = lambda_.Function(
            self,
            "GetStatsFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda/get_stats"),
            environment={"TABLE_NAME": self.table.table_name},
            timeout=Duration.seconds(10),
        )

        # 権限付与 - L2の便利メソッド
        self.table.grant_read_write_data(self.record_visit_lambda)
        self.table.grant_read_data(self.get_stats_lambda)

        # API Gateway
        self.api = apigateway.RestApi(
            self,
            "VisitorCounterApi",
            rest_api_name="Visitor Counter API",
        )

        visits_resource = self.api.root.add_resource("visits")
        visits_resource.add_method(
            "POST", apigateway.LambdaIntegration(self.record_visit_lambda)
        )

        stats_resource = visits_resource.add_resource("stats")
        stats_resource.add_method(
            "GET", apigateway.LambdaIntegration(self.get_stats_lambda)
        )

        # エスケープハッチ: API Gatewayのスロットリング設定
        # L2 Constructではメソッドレベルの詳細なスロットリング設定ができないため、
        # L1 Constructにアクセスして設定を追加
        cfn_stage = self.api.deployment_stage.node.default_child
        cfn_stage.add_property_override(
            "MethodSettings",
            [
                {
                    "HttpMethod": "*",
                    "ResourcePath": "/*",
                    "ThrottlingBurstLimit": 100,
                    "ThrottlingRateLimit": 50,
                }
            ],
        )
