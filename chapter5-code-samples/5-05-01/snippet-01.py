# ❌ 悪い例：パスワードとAPIキーが直接コードに書かれている
database = rds.DatabaseInstance(self, "Database",
    # ...
    credentials=rds.Credentials.from_password(
        username="admin",
        password="MySecretPassword123!"  # ❌ 絶対にやってはいけない
    )
)

lambda_function = lambda_.Function(self, "Function",
    # ...
    environment={
        "DB_PASSWORD": "MySecretPassword123!",  # ❌ 絶対にやってはいけない
        "API_KEY": "sk-1234567890abcdef"  # ❌ 絶対にやってはいけない
    }
)
