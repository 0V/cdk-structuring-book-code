from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class VisitorCounterAppStack(Stack):
    """DynamoDBテーブルを作成するStack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDBテーブルの作成
        self.table = dynamodb.Table(
            self,
            "VisitsTable",
            # パーティションキー: 訪問ID
            partition_key=dynamodb.Attribute(
                name="id", type=dynamodb.AttributeType.STRING
            ),
            # ソートキー: タイムスタンプ
            sort_key=dynamodb.Attribute(
                name="timestamp", type=dynamodb.AttributeType.STRING
            ),
            # オンデマンド課金モード
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            # Stack削除時にテーブルも削除（開発環境向け設定）
            removal_policy=RemovalPolicy.DESTROY,
        )
