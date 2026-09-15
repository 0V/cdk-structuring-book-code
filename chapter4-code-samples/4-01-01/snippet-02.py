class VpcConstruct(Construct):
    """VPCを管理するConstruct"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id)
        # VPC本体だけでなく、サブネット構成やフローログの設定もここにまとめる
        self.vpc = ec2.Vpc(self, "VPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Database",
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                    cidr_mask=24
                )
            ]
        )
        self.vpc.add_flow_log("FlowLog")

class SecurityGroupConstruct(Construct):
    """セキュリティグループを管理するConstruct"""
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id)
        self.database_sg = ec2.SecurityGroup(self, "DatabaseSG", vpc=vpc)
        self.app_sg = ec2.SecurityGroup(self, "AppSG", vpc=vpc)

class DatabaseConstruct(Construct):
    """データベースを管理するConstruct"""
    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc, security_group: ec2.SecurityGroup, **kwargs):
        super().__init__(scope, construct_id)
        self.database = rds.DatabaseInstance(self, "Database",
                                            vpc=vpc,
                                            security_groups=[security_group])

class ApiConstruct(Construct):
    """APIを管理するConstruct"""
    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc, database: DatabaseConstruct, **kwargs):
        super().__init__(scope, construct_id)
        self.function = lambda_.Function(self, "Function",
                                        vpc=vpc,
                                        environment={
                                            "DB_HOST": database.database.instance_endpoint.hostname
                                        })
