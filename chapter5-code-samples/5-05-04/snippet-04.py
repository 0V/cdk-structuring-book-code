from aws_cdk import aws_ssm as ssm

# Parameter Storeから共有VPC IDを取得
vpc_id = ssm.StringParameter.value_from_lookup(
    self, "/shared/vpc/production/id"
)

vpc = ec2.Vpc.from_lookup(self, "SharedVPC",
    vpc_id=vpc_id
)
