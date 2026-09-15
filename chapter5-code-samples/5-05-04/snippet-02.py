from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_elasticloadbalancingv2 as elbv2

# セキュリティチームが管理する証明書を参照
certificate = acm.Certificate.from_certificate_arn(
    self, "Certificate",
    certificate_arn="arn:aws:acm:ap-northeast-1:123456789012:certificate/abcd1234-5678-90ef-ghij-klmnopqrstuv"
)

# ALBで証明書を使用
alb = elbv2.ApplicationLoadBalancer(self, "ALB",
    vpc=vpc,
    internet_facing=True
)

listener = alb.add_listener("HttpsListener",
    port=443,
    certificates=[certificate],  # 参照した証明書を使用
    default_action=elbv2.ListenerAction.fixed_response(200)
)
