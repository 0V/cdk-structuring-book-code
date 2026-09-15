from aws_cdk import Stack, aws_ssm as ssm
from constructs import Construct
from visitor_counter_app.constructs.visitor_counter import VisitorCounterConstruct


class VisitorCounterStack(Stack):
    """訪問者カウンターStack（SSMパラメータパターン）"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.visitor_counter = VisitorCounterConstruct(self, "VisitorCounter")
        self.table = self.visitor_counter.table

        # SSMパラメータとして保存（他のStackから参照可能）
        ssm.StringParameter(self, "TableNameParameter",
            parameter_name="/visitor-counter/table-name",
            string_value=self.table.table_name,
            description="DynamoDB table name for visitor counter",
        )

        ssm.StringParameter(self, "TableArnParameter",
            parameter_name="/visitor-counter/table-arn",
            string_value=self.table.table_arn,
            description="DynamoDB table ARN for visitor counter",
        )
