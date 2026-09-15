# ✅ 良い例：Lambda Layersで依存ライブラリを分離
layer = lambda_.LayerVersion(self, "DependenciesLayer",
    code=lambda_.Code.from_asset("lambda-layer"),
    compatible_runtimes=[lambda_.Runtime.PYTHON_3_12]
)

lambda_.Function(self, "Function",
    code=lambda_.Code.from_asset("lambda"),  # アプリケーションコードのみ
    layers=[layer],  # 依存ライブラリはLayerから取得
    runtime=lambda_.Runtime.PYTHON_3_12
)
