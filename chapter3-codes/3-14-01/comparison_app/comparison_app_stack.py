from typing import Any

from aws_cdk import Stack
from aws_cdk import aws_s3 as s3
from constructs import Construct


class ComparisonAppStack(Stack):
    """開発環境の設定差を確認するための最小Stack。"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs: Any) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # コードの意図を明確にするため、S3マネージド暗号化を明示します。
        s3.Bucket(
            self,
            "SampleBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
        )
