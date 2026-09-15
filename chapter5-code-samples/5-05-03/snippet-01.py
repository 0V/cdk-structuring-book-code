# ✅ 良い例：Lambda関数の構造のみをCDKで定義
lambda_function = lambda_.Function(self, "Function",
    runtime=lambda_.Runtime.PYTHON_3_12,
    handler="index.handler",
    # 初回デプロイ用のプレースホルダー。実際のコードは別パイプラインが更新する
    code=lambda_.Code.from_inline("def handler(event, context): return {}"),
    memory_size=512,
    timeout=Duration.seconds(30),
    environment={
        "TABLE_NAME": table.table_name
    }
)

# ✅ 良い例：ECSタスクの構造のみをCDKで定義
task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
    memory_limit_mib=512,
    cpu=256
)

container = task_definition.add_container("app",
    image=ecs.ContainerImage.from_ecr_repository(
        repository=ecr_repository,
        # commitハッシュなど不変のタグを渡す。latestは使わない
        tag=self.node.try_get_context("image_tag")
    ),
    memory_limit_mib=512,
    logging=ecs.LogDrivers.aws_logs(stream_prefix="app")
)
