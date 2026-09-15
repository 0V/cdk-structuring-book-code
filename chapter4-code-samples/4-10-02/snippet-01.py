# 悪い例：1回しか使わないのに共通化
class SpecialUserTableConstruct(Construct):
    """特別なユーザーテーブル（実際は1回しか使わない）"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id)

        # 特殊な設定で、他では使わない
        self.table = dynamodb.Table(self, "UserTable",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            # 特殊な設定が続く...
        )

# 良い例：直接書く方がシンプル
class UserServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 特殊な用途なら直接定義する方が分かりやすい
        self.user_table = dynamodb.Table(self, "UserTable",
            partition_key=dynamodb.Attribute(name="user_id", type=dynamodb.AttributeType.STRING),
            # 設定内容が一目で分かる
        )
