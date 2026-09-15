# 共通化前：同じ設定を何度も書いている
class UserServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数の設定（毎回同じような内容）
        self.user_api = lambda_.Function(self, "UserAPI",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={"LOG_LEVEL": "INFO"}
        )

class OrderServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # また同じような設定を書いている
        self.order_api = lambda_.Function(self, "OrderAPI",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={"LOG_LEVEL": "INFO"}
        )

# 共通化後：共通のConstructを作成
class StandardLambdaConstruct(Construct):
    """よく使うLambda関数の設定をまとめたConstruct"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id)

        self.function = lambda_.Function(self, "Function",
            runtime=lambda_.Runtime.PYTHON_3_12,
            timeout=Duration.seconds(30),
            memory_size=256,
            environment={"LOG_LEVEL": "INFO"}
        )

# 使用例：コードがすっきりする
class UserServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.user_api = StandardLambdaConstruct(self, "UserAPI")

class OrderServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.order_api = StandardLambdaConstruct(self, "OrderAPI")
