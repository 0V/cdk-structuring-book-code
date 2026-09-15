# 悪い例：実験中のものを共通化
class ExperimentalApiConstruct(Construct):
    """実験中のAPI（設定がよく変わる）"""
    # 毎週設定が変わるので、共通化すると逆に面倒

# 良い例：安定するまで個別に管理
class ExperimentalServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 実験段階では個別に定義
        # 安定したら共通化を検討する
        self.experimental_api = apigateway.RestApi(self, "ExperimentalAPI")
