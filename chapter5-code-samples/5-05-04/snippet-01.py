from aws_cdk import aws_ec2 as ec2

# VPC IDを直接指定して既存VPCを参照
vpc = ec2.Vpc.from_lookup(self, "SharedVPC",
    vpc_id="vpc-0123456789abcdef0"  # 中央チームから提供されたVPC ID
)

# タグで検索して既存VPCを参照
vpc = ec2.Vpc.from_lookup(self, "SharedVPC",
    tags={
        "Environment": "production",
        "ManagedBy": "InfraTeam"
    }
)

# 参照したVPCを使用してリソースを作成
security_group = ec2.SecurityGroup(self, "AppSecurityGroup",
    vpc=vpc,  # 既存VPCを使用
    description="Application security group"
)
