from aws_cdk import aws_kms as kms
from aws_cdk import aws_rds as rds

# セキュリティチームが管理するKMSキーを参照
encryption_key = kms.Key.from_key_arn(
    self, "EncryptionKey",
    key_arn="arn:aws:kms:ap-northeast-1:123456789012:key/12345678-1234-1234-1234-123456789012"
)

# RDSインスタンスで暗号化キーを使用
database = rds.DatabaseInstance(self, "Database",
    engine=rds.DatabaseInstanceEngine.postgres(
        version=rds.PostgresEngineVersion.VER_17_5
    ),
    vpc=vpc,
    storage_encrypted=True,
    storage_encryption_key=encryption_key  # 参照したKMSキーを使用
)
