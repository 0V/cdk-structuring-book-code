from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    CfnOutput,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
from constructs import Construct


class VisitorCounterAppStack(Stack):

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

        # Lambda関数
        self.record_visit_lambda = lambda_.Function(
            self,
            "RecordVisitFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda/record_visit"),
            environment={"TABLE_NAME": self.table.table_name},
            timeout=Duration.seconds(10),
        )

        # DynamoDBへのアクセス権限を付与
        self.table.grant_read_write_data(self.record_visit_lambda)

        # API Gateway（新規追加）
        self.api = apigateway.RestApi(
            self,
            "VisitorCounterApi",
            rest_api_name="Visitor Counter API",
        )

        # /visits エンドポイント（新規追加）
        visits_resource = self.api.root.add_resource("visits")
        visits_resource.add_method(
            "POST", apigateway.LambdaIntegration(self.record_visit_lambda)
        )

        # APIエンドポイントを出力
        CfnOutput(self, "ApiEndpoint", value=self.api.url)
