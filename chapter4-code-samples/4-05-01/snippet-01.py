# 第1層: 基本的なConstruct
class BaseConstruct(Construct):
    """すべてのConstructの基底クラス"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id)

        # 共通のタグ付け
        self._apply_common_tags()

    def _apply_common_tags(self):
        """組織共通のタグを適用"""
        Tags.of(self).add("ManagedBy", "CDK")
        Tags.of(self).add("Organization", "MyCompany")

# 第2層: サービス固有のConstruct
class DatabaseConstruct(BaseConstruct):
    """データベース関連の基本Construct"""

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id)

        self.vpc = vpc
        self.security_group = self._create_security_group()

    def _create_security_group(self) -> ec2.SecurityGroup:
        return ec2.SecurityGroup(self, "SecurityGroup",
            vpc=self.vpc,
            description="Database security group"
        )

# 第3層: 具体的な実装Construct
class PostgreSQLConstruct(DatabaseConstruct):
    """PostgreSQL専用のConstruct"""

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc, instance_type: rds.InstanceType = None, **kwargs):
        super().__init__(scope, construct_id, vpc, **kwargs)

        self.instance_type = instance_type or rds.InstanceType.of(
            rds.InstanceClass.T3, rds.InstanceSize.MICRO
        )

        self.database = rds.DatabaseInstance(self, "Database",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_17_5
            ),
            instance_type=self.instance_type,
            vpc=self.vpc,
            security_groups=[self.security_group],
            backup_retention=Duration.days(7),
            deletion_protection=True
        )

class MySQLConstruct(DatabaseConstruct):
    """MySQL専用のConstruct"""

    def __init__(self, scope: Construct, construct_id: str,
                 vpc: ec2.Vpc, instance_type: rds.InstanceType = None, **kwargs):
        super().__init__(scope, construct_id, vpc, **kwargs)

        self.instance_type = instance_type or rds.InstanceType.of(
            rds.InstanceClass.T3, rds.InstanceSize.MICRO
        )

        self.database = rds.DatabaseInstance(self, "Database",
            engine=rds.DatabaseInstanceEngine.mysql(
                version=rds.MysqlEngineVersion.VER_8_0_28
            ),
            instance_type=self.instance_type,
            vpc=self.vpc,
            security_groups=[self.security_group],
            backup_retention=Duration.days(7),
            deletion_protection=True
        )
