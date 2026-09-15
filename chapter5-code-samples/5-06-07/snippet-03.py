# ❌ 悪い例：環境名のハードコーディング
class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 環境名がハードコーディングされている
        lambda_.Function(self, "Function",
            environment={
                "ENV": "dev",  # 本番環境でも "dev" になってしまう
                "DB_HOST": "dev-database.example.com"
            }
        )
