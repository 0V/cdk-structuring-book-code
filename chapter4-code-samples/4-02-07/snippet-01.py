# セキュリティチームが管理
class SecurityStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # IAMロール、ポリシー、KMSキーなど
        self.app_role = iam.Role(self, "AppRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        self.kms_key = kms.Key(self, "AppKey")

# ネットワークチームが管理
class NetworkStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC、サブネット、セキュリティグループなど
        self.vpc = ec2.Vpc(self, "VPC", max_azs=2)
        self.app_sg = ec2.SecurityGroup(self, "AppSG", vpc=self.vpc)

# アプリケーションチームが管理
class ApplicationStack(Stack):
    def __init__(self, scope, construct_id, security, network, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # セキュリティチームとネットワークチームが用意したリソースを使用
        self.function = lambda_.Function(self, "API",
            vpc=network.vpc,
            security_groups=[network.app_sg],
            role=security.app_role,
            environment_encryption=security.kms_key
        )
