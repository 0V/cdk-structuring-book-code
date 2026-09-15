class EnvironmentConfig:
    def __init__(self, env_name: str):
        self.env_name = env_name

    @property
    def db_instance_type(self) -> str:
        # 環境ごとに異なるインスタンスタイプを返す
        return {
            "dev": "t3.micro",
            "staging": "t3.small",
            "prod": "r5.large"
        }[self.env_name]

    @property
    def lambda_memory_size(self) -> int:
        # 環境ごとに異なるメモリサイズを返す
        return {
            "dev": 128,
            "staging": 256,
            "prod": 512
        }[self.env_name]
