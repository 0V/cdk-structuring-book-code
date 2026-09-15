from mycompany_constructs.database import PostgreSQLConstruct
from mycompany_constructs.compute import StandardLambdaConstruct
from mycompany_constructs.networking import StandardVpcConstruct
from aws_cdk import Stack, App
from constructs import Construct

class MyApplicationStack(Stack):
    """アプリケーションStack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 共通ライブラリのConstructを使用
        self.vpc = StandardVpcConstruct(self, "VPC",
            cidr="10.0.0.0/16"
        )

        self.database = PostgreSQLConstruct(self, "Database",
            vpc=self.vpc.vpc,
            instance_type=rds.InstanceType.of(
                rds.InstanceClass.T3,
                rds.InstanceSize.SMALL
            )
        )

        self.api = StandardLambdaConstruct(self, "API",
            config=LambdaConfig.for_api_service(),
            code_path="./lambda/api"
        )

# アプリケーションの起動
app = App()
MyApplicationStack(app, "MyApp")
app.synth()
