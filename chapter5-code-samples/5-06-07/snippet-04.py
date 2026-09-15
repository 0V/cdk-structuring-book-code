# ✅ 良い例：環境名をパラメータとして受け取る
class MyStack(Stack):
    def __init__(self, scope: Construct, id: str, env_name: str, config: dict, **kwargs):
        super().__init__(scope, id, **kwargs)

        # 環境ごとの設定を使用
        lambda_.Function(self, "Function",
            environment={
                "ENV": env_name,
                "DB_HOST": config["database"]["host"]
            }
        )
