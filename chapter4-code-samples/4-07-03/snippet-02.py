# 良い例: フラグで制御
class ApplicationStack(Stack):
    def __init__(self, scope, construct_id,
                 deploy_ecs: bool = False, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.ecr_repository = ecr.Repository(self, "AppRepository")

        if deploy_ecs:
            self.ecs_service = ecs.FargateService(self, "AppService", ...)

# 使用例
# 初回デプロイ: deploy_ecs=False でECRのみ作成
# イメージpush後: deploy_ecs=True でECSも作成
