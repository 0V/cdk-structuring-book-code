# 共通のログバケットを持つStack
class LoggingStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 複数のサービスから参照されるログバケット
        self.log_bucket = s3.Bucket(self, "LogBucket",
            bucket_name="my-app-logs",
            lifecycle_rules=[
                s3.LifecycleRule(
                    expiration=Duration.days(90)
                )
            ]
        )

class ApplicationStack(Stack):
    def __init__(self, scope, construct_id, log_bucket, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ALBのアクセスログをログバケットに出力
        self.alb = elbv2.ApplicationLoadBalancer(self, "ALB", ...)
        self.alb.log_access_logs(log_bucket, prefix="alb")

class CloudFrontStack(Stack):
    def __init__(self, scope, construct_id, log_bucket, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # CloudFrontのログも同じバケットに出力
        self.distribution = cloudfront.Distribution(self, "CDN",
            log_bucket=log_bucket,
            log_file_prefix="cloudfront/"
        )

# 使用例
app = App()
logging = LoggingStack(app, "Logging")
application = ApplicationStack(app, "Application", log_bucket=logging.log_bucket)
cdn = CloudFrontStack(app, "CloudFront", log_bucket=logging.log_bucket)
