# ✅ 良い例：Secrets Managerで自動生成されたパスワードを使用
database = rds.DatabaseInstance(self, "Database",
    # ...
    credentials=rds.Credentials.from_generated_secret("admin")  # 自動生成
)

# ✅ 良い例：既存のSecrets Managerから外部APIキーを参照
external_api_secret = secretsmanager.Secret.from_secret_name_v2(
    self, "ExternalApiSecret",
    secret_name="prod/external-api/key"
)

# ✅ 良い例：機密情報のARNのみを環境変数に設定
lambda_function = lambda_.Function(self, "Function",
    # ...
    environment={
        "DB_SECRET_ARN": database.secret.secret_arn,  # ARNのみ
        "API_SECRET_ARN": external_api_secret.secret_arn
    }
)

# Lambda関数に機密情報へのアクセス権限を付与
database.secret.grant_read(lambda_function)
external_api_secret.grant_read(lambda_function)
