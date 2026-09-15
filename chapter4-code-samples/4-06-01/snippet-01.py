# 基盤Stack群
class NetworkStack(Stack):
    """ネットワーク基盤Stack"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPCとネットワーク関連の基盤
        self.vpc = ec2.Vpc(self, "VPC",
            max_azs=2,
            cidr="10.0.0.0/16",
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

        # セキュリティグループの基盤
        self.security_groups = SecurityGroupConstruct(self, "SecurityGroups",
                                                     vpc=self.vpc)

        # VPCエンドポイント
        self.vpc_endpoints = VpcEndpointConstruct(self, "VpcEndpoints",
                                                 vpc=self.vpc)

class SecurityStack(Stack):
    """セキュリティ基盤Stack"""
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # WAF
        self.waf = wafv2.CfnWebACL(self, "WebACL", ...)

        # Certificate Manager
        self.certificate = certificatemanager.Certificate(self, "Certificate", ...)

        # KMS
        self.kms_key = kms.Key(self, "KMSKey", ...)

class DataStack(Stack):
    """データ基盤Stack"""
    def __init__(self, scope: Construct, construct_id: str,
                 network: NetworkStack, security: SecurityStack, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # RDS
        self.database = rds.DatabaseInstance(self, "Database",
            vpc=network.vpc,
            security_groups=[network.security_groups.database_sg],
            storage_encrypted=True,
            storage_encryption_key=security.kms_key
        )

        # ElastiCache
        self.cache = elasticache.CfnCacheCluster(self, "Cache", ...)

        # DynamoDB
        self.user_table = dynamodb.Table(self, "UserTable",
            encryption=dynamodb.TableEncryption.CUSTOMER_MANAGED,
            encryption_key=security.kms_key
        )

# アプリケーションStack群
class UserServiceStack(Stack):
    """ユーザーサービス"""
    def __init__(self, scope: Construct, construct_id: str,
                 network: NetworkStack, data: DataStack, security: SecurityStack, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ユーザー管理API
        self.user_api = lambda_.Function(self, "UserAPI",
            vpc=network.vpc,
            security_groups=[network.security_groups.lambda_sg],
            environment={
                "DB_HOST": data.database.instance_endpoint.hostname,
                "USER_TABLE": data.user_table.table_name
            }
        )

        # API Gateway
        self.api_gateway = apigateway.RestApi(self, "UserApiGateway")

        # CloudFront
        self.distribution = cloudfront.Distribution(self, "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.RestApiOrigin(self.api_gateway)
            ),
            certificate=security.certificate,
            web_acl_id=security.waf.attr_arn
        )

class OrderServiceStack(Stack):
    """注文サービス"""
    def __init__(self, scope: Construct, construct_id: str,
                 network: NetworkStack, data: DataStack, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 注文処理API
        self.order_api = lambda_.Function(self, "OrderAPI",
            vpc=network.vpc,
            environment={
                "DB_HOST": data.database.instance_endpoint.hostname,
                "CACHE_ENDPOINT": data.cache.attr_redis_endpoint_address
            }
        )

        # SQS for order processing
        self.order_queue = sqs.Queue(self, "OrderQueue")

        # Order processor
        self.order_processor = lambda_.Function(self, "OrderProcessor",
            vpc=network.vpc,
            events=[lambda_event_sources.SqsEventSource(self.order_queue)]
        )
