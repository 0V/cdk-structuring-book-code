from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_ssm as ssm

# Secrets Managerから機密情報を参照
db_secret = secretsmanager.Secret.from_secret_name_v2(
    self, "DBSecret",
    secret_name="prod/database/password"
)

# Parameter Storeから設定値を参照
api_key = ssm.StringParameter.from_secure_string_parameter_attributes(
    self, "ApiKey",
    parameter_name="/prod/api/key"
)

# Lambda関数で機密情報を使用
lambda_function = lambda_.Function(self, "Function",
    # ... 他の設定 ...
    environment={
        "DB_SECRET_ARN": db_secret.secret_arn,  # ARNのみを環境変数に設定
        "API_KEY_PARAM": api_key.parameter_name
    }
)

# Lambda関数に機密情報へのアクセス権限を付与
db_secret.grant_read(lambda_function)
api_key.grant_read(lambda_function)
