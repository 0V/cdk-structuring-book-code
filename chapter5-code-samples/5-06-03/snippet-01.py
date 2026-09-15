from aws_cdk import App, Environment
from constructs import Construct

app = App()

# コンテキスト変数から環境名を取得
env_name = app.node.try_get_context("env")

if env_name is None:
    raise ValueError("環境名を指定してください: --context env=dev|staging|prod")

# 環境ごとの設定を読み込む
config = load_config(env_name)

# Stackを作成
MyStack(app, f"MyApp-{env_name}",
    env=Environment(
        account=config["account"],
        region=config["region"]
    ),
    config=config
)
