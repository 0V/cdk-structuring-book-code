from aws_cdk import aws_ec2 as ec2
from cdk_nag import NagSuppressions

class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # セキュリティグループの作成
        security_group = ec2.SecurityGroup(
            self, "MySecurityGroup",
            vpc=vpc,
            description="Security group for web servers"
        )

        # インターネット全体からのHTTPSアクセスを許可 (これはcdk-nagで警告される)
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(443),
            "Allow HTTPS from anywhere"
        )

        # ルールの抑制（理由を明記）
        NagSuppressions.add_resource_suppressions(
            security_group,
            [
                {
                    "id": "AwsSolutions-EC23",
                    "reason": "Public website must accept HTTPS access from any source"
                }
            ]
        )
