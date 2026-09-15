# リソース数を考慮した分割
class LambdaFunctionsStack(Stack):
    """Lambda関数専用Stack（20-30個程度に制限）"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 関連するLambda関数のみをグループ化
        self.user_functions = self._create_user_functions()      # 5個
        self.order_functions = self._create_order_functions()    # 8個
        self.notification_functions = self._create_notification_functions()  # 3個
        # 合計16個のLambda関数

class DatabaseStack(Stack):
    """データベース専用Stack"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # データベース関連リソースのみ
        self.user_table = dynamodb.Table(self, "UserTable", ...)
        self.order_table = dynamodb.Table(self, "OrderTable", ...)
        self.session_table = dynamodb.Table(self, "SessionTable", ...)
        # 合計10個程度のリソース

class StorageStack(Stack):
    """ストレージ専用Stack"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ストレージ関連リソースのみ
        self.user_data_bucket = s3.Bucket(self, "UserDataBucket", ...)
        self.order_data_bucket = s3.Bucket(self, "OrderDataBucket", ...)
        self.log_bucket = s3.Bucket(self, "LogBucket", ...)
        # 合計8個程度のリソース
