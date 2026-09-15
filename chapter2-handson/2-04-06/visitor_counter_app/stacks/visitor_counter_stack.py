from aws_cdk import Stack
from constructs import Construct
from visitor_counter_app.constructs.visitor_counter import VisitorCounterConstruct


class VisitorCounterStack(Stack):
    """訪問者カウンターStack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.visitor_counter = VisitorCounterConstruct(self, "VisitorCounter")
