import aws_cdk as cdk
from aws_cdk import assertions

from comparison_app.comparison_app_stack import ComparisonAppStack


def test_bucket_security_settings() -> None:
    app = cdk.App()
    stack = ComparisonAppStack(app, "TestStack")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::S3::Bucket",
        {"BucketEncryption": assertions.Match.any_value()},
    )
    template.resource_count_is("AWS::S3::BucketPolicy", 1)
