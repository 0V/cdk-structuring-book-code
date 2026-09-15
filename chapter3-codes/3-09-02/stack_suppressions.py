# Stack全体で特定のルールを抑制
NagSuppressions.add_stack_suppressions(
    self,
    [
        {
            "id": "AwsSolutions-IAM4",
            "reason": "AWS managed policies are acceptable for this use case"
        },
        {
            "id": "AwsSolutions-IAM5",
            "reason": "Wildcard permissions needed for CloudFormation deployment role"
        }
    ]
)
