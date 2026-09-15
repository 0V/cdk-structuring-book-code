class TestableConstruct(Construct):
    """テスト可能なConstruct"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id)

        # 内部リソースを型付きの公開属性として保持する
        self.vpc = self._create_vpc()
        self.database = self._create_database()

    def _create_vpc(self) -> ec2.Vpc:
        """VPCを作成"""
        return ec2.Vpc(self, "VPC", max_azs=2)

    def _create_database(self) -> rds.DatabaseInstance:
        """データベースを作成"""
        return rds.DatabaseInstance(self, "Database",
            vpc=self.vpc,
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_17_5
            ),
            multi_az=True
        )

# テストコード例
import pytest
from aws_cdk import App, Stack

def test_testable_construct():
    """TestableConstructのテスト"""
    app = App()
    stack = Stack(app, "TestStack")

    construct = TestableConstruct(stack, "TestConstruct")

    # リソースが正しく作成されているかテスト
    assert construct.vpc is not None
    assert construct.database is not None

    # VPCの設定をテスト
    assert construct.vpc.max_azs == 2

    # データベースの設定をテスト
    assert construct.database.engine.engine_type == "postgres"
