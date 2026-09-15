"""
L1 Construct版: 訪問者カウンターのConstruct

L1 Constructは CloudFormation リソースの1対1マッピングです。
クラス名が Cfn で始まり、CloudFormation の全プロパティにアクセス可能ですが、
CDK独自の便利機能（自動的なIAMロール作成など）は利用できません。
"""
from aws_cdk import (
    RemovalPolicy,
    Duration,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_s3_assets as s3_assets,
)
from constructs import Construct


class VisitorCounterConstruct(Construct):
    """訪問者カウンターのConstruct（L1 Construct版）"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ===========================================
        # L1 Construct: DynamoDBテーブル (CfnTable)
        # ===========================================
        # L1ではすべてのプロパティを明示的に指定する必要がある
        self.cfn_table = dynamodb.CfnTable(
            self,
            "VisitsTable",
            table_name=None,  # CDKに自動生成させる
            key_schema=[
                dynamodb.CfnTable.KeySchemaProperty(
                    attribute_name="id",
                    key_type="HASH"  # パーティションキー
                ),
                dynamodb.CfnTable.KeySchemaProperty(
                    attribute_name="timestamp",
                    key_type="RANGE"  # ソートキー
                ),
            ],
            attribute_definitions=[
                dynamodb.CfnTable.AttributeDefinitionProperty(
                    attribute_name="id",
                    attribute_type="S"  # String型
                ),
                dynamodb.CfnTable.AttributeDefinitionProperty(
                    attribute_name="timestamp",
                    attribute_type="S"  # String型
                ),
            ],
            billing_mode="PAY_PER_REQUEST",  # オンデマンド課金
        )
        # L1ではRemovalPolicyを直接設定できないため、
        # CloudFormationのDeletionPolicyを使用
        self.cfn_table.apply_removal_policy(RemovalPolicy.DESTROY)

        # ===========================================
        # L1 Construct: Lambda実行ロール (CfnRole)
        # L2では自動作成されるが、L1では手動で作成が必要
        # ===========================================
        self.lambda_role = iam.CfnRole(
            self,
            "LambdaExecutionRole",
            assume_role_policy_document={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": "lambda.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }
                ]
            },
            managed_policy_arns=[
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
            ],
            policies=[
                iam.CfnRole.PolicyProperty(
                    policy_name="DynamoDBAccess",
                    policy_document={
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": ["dynamodb:PutItem"],
                                "Resource": self.cfn_table.attr_arn
                            }
                        ]
                    }
                )
            ]
        )

        # ===========================================
        # L1 Construct: Lambda関数 (CfnFunction)
        # ===========================================
        record_visit_asset = s3_assets.Asset(
            self, "RecordVisitCode", path="lambda/record_visit"
        )

        self.record_visit_lambda = lambda_.CfnFunction(
            self,
            "RecordVisitFunction",
            runtime="python3.12",
            handler="index.handler",
            code=lambda_.CfnFunction.CodeProperty(
                s3_bucket=record_visit_asset.s3_bucket_name,
                s3_key=record_visit_asset.s3_object_key,
            ),
            role=self.lambda_role.attr_arn,
            timeout=10,
            environment=lambda_.CfnFunction.EnvironmentProperty(
                variables={"TABLE_NAME": self.cfn_table.ref}
            ),
        )

        get_stats_asset = s3_assets.Asset(
            self, "GetStatsCode", path="lambda/get_stats"
        )

        self.get_stats_lambda = lambda_.CfnFunction(
            self,
            "GetStatsFunction",
            runtime="python3.12",
            handler="index.handler",
            code=lambda_.CfnFunction.CodeProperty(
                s3_bucket=get_stats_asset.s3_bucket_name,
                s3_key=get_stats_asset.s3_object_key,
            ),
            role=self.lambda_role.attr_arn,
            timeout=10,
            environment=lambda_.CfnFunction.EnvironmentProperty(
                variables={"TABLE_NAME": self.cfn_table.ref}
            ),
        )

        # ===========================================
        # L2 Construct: API Gateway
        # API Gatewayは L1 で書くとリソース数が多く冗長になるため L2 を使う
        # ===========================================
        self.api = apigateway.RestApi(
            self,
            "VisitorCounterApi",
            rest_api_name="Visitor Counter API",
        )

        # L1 で作った関数を L2 の統合に渡すため、ARN から IFunction を得る
        record_visit_fn = lambda_.Function.from_function_arn(
            self, "RecordVisitFn", self.record_visit_lambda.attr_arn
        )
        get_stats_fn = lambda_.Function.from_function_arn(
            self, "GetStatsFn", self.get_stats_lambda.attr_arn
        )

        visits_resource = self.api.root.add_resource("visits")
        visits_resource.add_method(
            "POST", apigateway.LambdaIntegration(record_visit_fn)
        )

        stats_resource = visits_resource.add_resource("stats")
        stats_resource.add_method(
            "GET", apigateway.LambdaIntegration(get_stats_fn)
        )

        # from_function_arn で参照した関数には呼び出し許可が自動で付かないため、
        # L1 の CfnPermission で明示的に付与する
        lambda_.CfnPermission(
            self,
            "RecordVisitApiPermission",
            action="lambda:InvokeFunction",
            function_name=self.record_visit_lambda.ref,
            principal="apigateway.amazonaws.com",
            source_arn=self.api.arn_for_execute_api(),
        )

        lambda_.CfnPermission(
            self,
            "GetStatsApiPermission",
            action="lambda:InvokeFunction",
            function_name=self.get_stats_lambda.ref,
            principal="apigateway.amazonaws.com",
            source_arn=self.api.arn_for_execute_api(),
        )
