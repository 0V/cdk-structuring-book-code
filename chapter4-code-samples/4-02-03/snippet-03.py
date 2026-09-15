class SecurityTeamConstruct(Construct):
    """セキュリティチームが管理するリソース"""
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        # セキュリティチームの責任範囲のリソース
        self.waf = wafv2.CfnWebACL(self, "WAF",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope="REGIONAL",
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True,
                metric_name="WAFMetrics",
                sampled_requests_enabled=True))
        self.kms_key = kms.Key(self, "Key",
            enable_key_rotation=True)

class NetworkTeamConstruct(Construct):
    """ネットワークチームが管理するリソース"""
    def __init__(self, scope: Construct, construct_id: str):
        super().__init__(scope, construct_id)

        # ネットワークチームの責任範囲のリソース
        self.vpc = ec2.Vpc(self, "VPC", max_azs=2)
        self.app_sg = ec2.SecurityGroup(self, "AppSG", vpc=self.vpc)
        self.db_sg = ec2.SecurityGroup(self, "DBSG", vpc=self.vpc)
