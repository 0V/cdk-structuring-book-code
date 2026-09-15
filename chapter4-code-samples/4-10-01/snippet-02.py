# 組織標準のVPC設定を共通化
class CompanyStandardVpc(Construct):
    """会社標準のVPC設定"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id)

        self.vpc = ec2.Vpc(self, "VPC",
            cidr="10.0.0.0/16",
            max_azs=2,
            # 会社で決められた標準設定
            enable_dns_hostnames=True,
            enable_dns_support=True
        )

        # 会社標準のタグを自動で付与
        Tags.of(self.vpc).add("Organization", "MyCompany")
        Tags.of(self.vpc).add("ManagedBy", "CDK")
