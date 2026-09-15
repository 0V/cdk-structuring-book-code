# 良い例：依存関係を一方向にする
class NetworkStack(Stack):
    """基盤となるネットワークリソース"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc(self, "VPC", max_azs=2)
        # セキュリティグループも基盤として定義
        self.db_security_group = ec2.SecurityGroup(self, "DBSecurityGroup", vpc=self.vpc)
        self.app_security_group = ec2.SecurityGroup(self, "AppSecurityGroup", vpc=self.vpc)

class DatabaseStack(Stack):
    """データベースリソース（ネットワークに依存）"""
    def __init__(self, scope, construct_id, network_stack: NetworkStack, **kwargs):
        # ... NetworkStackのみを参照

class ApplicationStack(Stack):
    """アプリケーションリソース（ネットワークとデータベースに依存）"""
    def __init__(self, scope, construct_id, network_stack: NetworkStack,
                 database_stack: DatabaseStack, **kwargs):
        # ... NetworkStackとDatabaseStackを参照

# 依存関係が明確で循環参照が発生しない
# Network → Database → Application の一方向依存
app = App()
network = NetworkStack(app, "Network")
database = DatabaseStack(app, "Database", network)
application = ApplicationStack(app, "Application", network, database)
