class WebServerConstruct(Construct):
    """Webサーバーに必要なリソースをまとめたConstruct"""
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc):
        super().__init__(scope, construct_id)

        # Webサーバー関連のリソースをまとめて定義
        self.security_group = ec2.SecurityGroup(self, "SG", vpc=vpc)
        self.instance = ec2.Instance(self, "Instance",
                                    vpc=vpc,
                                    security_group=self.security_group)
        self.target_group = elbv2.ApplicationTargetGroup(self, "TargetGroup",
                                                        vpc=vpc,
                                                        targets=[self.instance])
