from aws_cdk import Stack
from constructs import Construct


class VisitorCounterAppStack(Stack):
    """訪問者カウンターアプリケーションのStack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ここにリソースを追加していきます
        pass
