# ❌ 推奨しない：desired_countを明示的に指定
service = ecs.FargateService(self, "Service",
    cluster=cluster,
    task_definition=task_definition,
    desired_count=3  # Auto Scalingで5に増えても、次回デプロイ時に3に戻る可能性
)
