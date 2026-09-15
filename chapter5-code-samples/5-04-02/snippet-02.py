import json

# 設定ファイルを読み込む
with open(f"config/{env_name}.json") as f:
    config = json.load(f)

# 設定値を使用してリソースを定義
rds.DatabaseInstance(self, "Database",
    instance_type=ec2.InstanceType(config["database"]["instanceType"]),
    multi_az=config["database"]["multiAz"]
)
