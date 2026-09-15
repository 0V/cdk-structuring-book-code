# ECRリポジトリ専用Stack
class ContainerRegistryStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        self.ecr_repository = ecr.Repository(self, "AppRepository")

# ECSサービス専用Stack
class EcsServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ECRリポジトリを参照
        repository_uri = Fn.import_value("AppRepositoryUri")

        # ECSサービスを定義
        self.service = ecs.FargateService(self, "Service",
            task_definition=ecs.FargateTaskDefinition(self, "TaskDef",
                container_definitions=[{
                    "image": f"{repository_uri}:latest"
                }]
            )
        )
