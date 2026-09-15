class EverythingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "VPC", max_azs=2)

        # セキュリティグループ
        web_sg = ec2.SecurityGroup(self, "WebSG", vpc=vpc)
        db_sg = ec2.SecurityGroup(self, "DBSG", vpc=vpc)

        # データベース
        database = rds.DatabaseInstance(self, "DB", ...)

        # Lambda関数
        api_function = lambda_.Function(self, "API", ...)
        auth_function = lambda_.Function(self, "Auth", ...)

        # API Gateway
        api = apigateway.RestApi(self, "API", ...)

        # S3バケット
        data_bucket = s3.Bucket(self, "Data", ...)
        log_bucket = s3.Bucket(self, "Log", ...)

        # CloudFront
        distribution = cloudfront.Distribution(self, "CDN", ...)

        # ... さらに続く
