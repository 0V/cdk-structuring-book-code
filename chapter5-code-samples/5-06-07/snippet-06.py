# ✅ 良い例：本番環境ではRETAINを設定
from aws_cdk import RemovalPolicy

database = rds.DatabaseInstance(self, "Database",
    # ...
    removal_policy=RemovalPolicy.RETAIN if env_name == "prod" else RemovalPolicy.DESTROY
)

# S3バケットも同様
bucket = s3.Bucket(self, "Bucket",
    removal_policy=RemovalPolicy.RETAIN if env_name == "prod" else RemovalPolicy.DESTROY,
    auto_delete_objects=False if env_name == "prod" else True
)
