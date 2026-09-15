# 組み合わせ例
class ECommerceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 1. まず担当者カットで大きく分割
        self.network = NetworkTeamConstruct(self, "Network")

        # 2. 機能別にコンポーネントカット
        self.user_service = UserServiceConstruct(self, "UserService",
            network_config=self.network.get_network_config()
        )

        self.order_service = OrderServiceConstruct(self, "OrderService",
            network_config=self.network.get_network_config()
        )

        # 3. 必要に応じてリソースグループカット
        self.monitoring = MonitoringConstruct(self, "Monitoring",
            resources_to_monitor=[
                self.user_service.get_monitorable_resources(),
                self.order_service.get_monitorable_resources()
            ]
        )
