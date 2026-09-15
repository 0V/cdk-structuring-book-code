# ❌ 悪い例：すべての依存ライブラリを関数のパッケージに含めている
lambda_.Function(self, "Function",
    code=lambda_.Code.from_asset("lambda",
        bundling=BundlingOptions(
            image=lambda_.Runtime.PYTHON_3_12.bundling_image,
            command=[
                "bash", "-c",
                "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
            ]
        )
    )
)
