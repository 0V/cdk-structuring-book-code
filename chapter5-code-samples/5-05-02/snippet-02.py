# ✅ 良い例：desired_countを指定せず、スケーリングポリシーのみ定義
service = ecs.FargateService(self, "Service",
    cluster=cluster,
    task_definition=task_definition,
    # desired_countを指定しない（デフォルト値1が使用される）
)

# スケーリングポリシーを定義
scaling = service.auto_scale_task_count(
    min_capacity=1,
    max_capacity=10
)

scaling.scale_on_cpu_utilization("CpuScaling",
    target_utilization_percent=70
)
