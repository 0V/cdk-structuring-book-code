# 悪い例：手動作成リソースとCDK管理リソースの混在
class ProblematicStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 手動で作成されたVPCを参照
        existing_vpc = ec2.Vpc.from_lookup(self, "ExistingVPC",
            vpc_id="vpc-12345678"  # 手動で作成されたVPC
        )

        # CDKで新しいリソースを作成
        self.database = rds.DatabaseInstance(self, "Database",
            vpc=existing_vpc  # 手動VPCに依存
        )

        # 手動で作成されたセキュリティグループを参照
        existing_sg = ec2.SecurityGroup.from_security_group_id(
            self, "ExistingSG", "sg-87654321"
        )

        self.lambda_function = lambda_.Function(self, "Function",
            vpc=existing_vpc,
            security_groups=[existing_sg]  # 手動SGに依存
        )
