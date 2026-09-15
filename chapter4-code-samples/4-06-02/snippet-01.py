# 環境別設定の定義
@dataclass
class EnvironmentConfig:
    environment_name: str
    vpc_cidr: str
    db_instance_type: str
    db_backup_retention_days: int
    db_multi_az: bool
    lambda_memory_size: int

# 開発環境の設定
dev_config = EnvironmentConfig(
    environment_name="development",
    vpc_cidr="10.0.0.0/16",
    db_instance_type="db.t3.micro",
    db_backup_retention_days=1,
    db_multi_az=False,
    lambda_memory_size=128
)

# 本番環境の設定
prod_config = EnvironmentConfig(
    environment_name="production",
    vpc_cidr="10.2.0.0/16",
    db_instance_type="db.r5.large",
    db_backup_retention_days=30,
    db_multi_az=True,
    lambda_memory_size=512
)

# 各環境のStageを作成
app = App()
dev_stage = MyApplicationStage(app, "Development", dev_config)
prod_stage = MyApplicationStage(app, "Production", prod_config)
