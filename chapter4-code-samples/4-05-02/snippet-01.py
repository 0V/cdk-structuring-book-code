from dataclasses import dataclass, field
from aws_cdk import Duration
from aws_cdk.aws_lambda import Runtime, Tracing

@dataclass
class LambdaConfig:
    """Lambda関数の設定を定義するクラス"""
    runtime: Runtime = Runtime.PYTHON_3_12
    timeout: Duration = Duration.seconds(30)
    memory_size: int = 256
    environment: dict = field(default_factory=dict)
    tracing: Tracing = Tracing.ACTIVE

    @classmethod
    def for_api_service(cls) -> 'LambdaConfig':
        """APIサービス用の設定"""
        return cls(
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={"SERVICE_TYPE": "api"}
        )

    @classmethod
    def for_batch_service(cls) -> 'LambdaConfig':
        """バッチサービス用の設定"""
        return cls(
            timeout=Duration.minutes(15),
            memory_size=1024,
            environment={"SERVICE_TYPE": "batch"}
        )

class ConfigurableLambdaConstruct(Construct):
    """設定可能なLambda関数のConstruct"""

    def __init__(self, scope: Construct, construct_id: str,
                 config: LambdaConfig, code_path: str, **kwargs):
        super().__init__(scope, construct_id)

        self.function = lambda_.Function(self, "Function",
            runtime=config.runtime,
            handler="index.handler",
            code=lambda_.Code.from_asset(code_path),
            timeout=config.timeout,
            memory_size=config.memory_size,
            environment=config.environment,
            tracing=config.tracing,
            **kwargs
        )

# 使用例
api_lambda = ConfigurableLambdaConstruct(self, "ApiLambda",
    config=LambdaConfig.for_api_service(),
    code_path="./lambda/api"
)

batch_lambda = ConfigurableLambdaConstruct(self, "BatchLambda",
    config=LambdaConfig.for_batch_service(),
    code_path="./lambda/batch"
)
