# 悪い例：循環参照が発生
class DatabaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,
                 application_stack: 'ApplicationStack', **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # アプリケーションStackのセキュリティグループを参照
        self.database = rds.DatabaseInstance(self, "Database",
            vpc=application_stack.vpc,
            security_groups=[application_stack.db_security_group]  # 参照1
        )

class ApplicationStack(Stack):
    def __init__(self, scope: Construct, construct_id: str,
                 database_stack: DatabaseStack, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "VPC")
        self.db_security_group = ec2.SecurityGroup(self, "DBSecurityGroup", vpc=self.vpc)

        # データベースStackのデータベースを参照
        self.lambda_function = lambda_.Function(self, "Function",
            environment={
                "DB_HOST": database_stack.database.instance_endpoint.hostname  # 参照2
            }
        )

# これは動作しない！循環参照エラーが発生
app = App()
db_stack = DatabaseStack(app, "Database", app_stack)  # app_stackがまだ定義されていない
app_stack = ApplicationStack(app, "Application", db_stack)  # db_stackがapp_stackを参照している
