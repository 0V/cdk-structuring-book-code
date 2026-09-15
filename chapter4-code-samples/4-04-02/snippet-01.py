# ライフサイクルによる分割例
class StatefulStack(Stack):
    """データを保持するリソース (削除保護あり)"""
    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # データを保持するリソース: 誤削除によるデータ損失を防ぐ
        self.database = rds.DatabaseInstance(self, "Database",
            vpc=vpc,
            deletion_protection=True,  # 削除保護を有効化
            backup_retention=Duration.days(30)
        )

        self.data_bucket = s3.Bucket(self, "DataBucket",
            versioned=True,
            removal_policy=RemovalPolicy.RETAIN  # Stack削除時もバケットを保持
        )

class InfrastructureStack(Stack):
    """ネットワーク基盤 (滅多に変更しない)"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ネットワーク基盤: 多くのリソースが依存するため安定性を重視
        self.vpc = ec2.Vpc(self, "VPC", max_azs=2)

class ApplicationStack(Stack):
    """アプリケーション (リリースのたびに更新)"""
    def __init__(self, scope: Construct, construct_id: str,
                 infra: InfrastructureStack,
                 stateful: StatefulStack, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 頻繁に更新されるリソース
        self.api_function = lambda_.Function(self, "ApiFunction",
            vpc=infra.vpc,
            environment={
                "DB_HOST": stateful.database.instance_endpoint.hostname
            }
        )
        self.api_gateway = apigateway.RestApi(self, "ApiGateway")
