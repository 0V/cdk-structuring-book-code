from aws_cdk import Stack, CfnOutput
from constructs import Construct
from visitor_counter_app.constructs.visitor_counter import VisitorCounterConstruct


class VisitorCounterStack(Stack):
    """訪問者カウンターStack（Fn::ImportValue/Exportパターン）"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.visitor_counter = VisitorCounterConstruct(self, "VisitorCounter")
        self.table = self.visitor_counter.table

        # テーブル名をエクスポート（他のStackから参照可能にする）
        CfnOutput(self, "VisitsTableName",
            value=self.table.table_name,
            export_name="VisitorCounter-TableName",
        )

        # テーブルARNをエクスポート
        CfnOutput(self, "VisitsTableArn",
            value=self.table.table_arn,
            export_name="VisitorCounter-TableArn",
        )
