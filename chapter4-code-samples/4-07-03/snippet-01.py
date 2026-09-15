# 悪い例: コメントアウトで段階的デプロイ
class ApplicationStack(Stack):
    def __init__(self, scope, construct_id, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Step 1: まずECRリポジトリを作成
        self.ecr_repository = ecr.Repository(self, "AppRepository")

        # Step 2: イメージをpushした後、コメントを外してECSを作成
        # self.ecs_service = ecs.FargateService(self, "AppService",
        #     task_definition=ecs.FargateTaskDefinition(self, "TaskDef",
        #         ...
        #         container_definitions=[{
        #             "image": self.ecr_repository.repository_uri + ":latest"
        #         }]
        #     )
        # )
