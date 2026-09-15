from aws_cdk import RemovalPolicy, Stack, aws_s3 as s3
from constructs import Construct


class ImportDemoStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        bucket_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 取り込み対象の S3 バケット。既存の設定と一致させる必要がある。
        s3.Bucket(
            self,
            "ImportedBucket",
            # 物理IDを明示: cdk import 時の対話プロンプトを省略できる
            bucket_name=bucket_name,
            # バージョニング (既存バケットの設定と一致)
            versioned=True,
            # サーバーサイド暗号化 (S3 マネージドキー)
            encryption=s3.BucketEncryption.S3_MANAGED,
            # パブリックアクセスブロック (全項目 True)
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            # 誤削除防止: cdk destroy 時もバケットを残す
            removal_policy=RemovalPolicy.RETAIN,
        )
