# 悪い例: 循環参照
class DatabaseStack(Stack):
    def __init__(self, scope, construct_id, app_stack, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        # ApplicationStackを参照
        self.database = rds.DatabaseInstance(self, "DB",
            security_groups=[app_stack.db_security_group])

class ApplicationStack(Stack):
    def __init__(self, scope, construct_id, db_stack, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        # DatabaseStackを参照
        self.function = lambda_.Function(self, "API",
            environment={"DB_HOST": db_stack.database.instance_endpoint.hostname})

# エラー: 互いに参照し合っているためデプロイ不可
