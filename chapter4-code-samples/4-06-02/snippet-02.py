# 設定を読み込んでリソースを作成
config = ConfigLoader.load_config(environment)
self.database = rds.DatabaseInstance(self, "Database",
    instance_type=rds.InstanceType.of_instance_type_identifier(
        config["database"]["instance_class"]
    ),
    backup_retention=Duration.days(config["database"]["backup_retention_days"]),
    multi_az=config["database"]["multi_az"]
)
