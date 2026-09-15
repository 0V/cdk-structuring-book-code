# 悪い例：リソース数が多すぎるStack
class MassiveStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 大量のLambda関数（100個以上）
        for i in range(100):
            lambda_.Function(self, f"Function{i}", ...)

        # 大量のDynamoDBテーブル（50個以上）
        for i in range(50):
            dynamodb.Table(self, f"Table{i}", ...)

        # 大量のS3バケット（30個以上）
        for i in range(30):
            s3.Bucket(self, f"Bucket{i}", ...)

        # 合計180個のリソース（まだ制限内だが管理困難）
