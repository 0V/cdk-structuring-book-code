from aws_cdk import Stack
from constructs import Construct
from visitor_counter_app.constructs.visitor_counter import VisitorCounterConstruct


class VisitorCounterStack(Stack):
    """訪問者カウンターStack（クロスStack参照パターン）"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.visitor_counter = VisitorCounterConstruct(self, "VisitorCounter")

        # 他のStackから参照できるように属性を公開
        self.table = self.visitor_counter.table
        self.api = self.visitor_counter.api
