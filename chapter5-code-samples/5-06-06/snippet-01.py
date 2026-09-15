from aws_cdk import aws_rds as rds

# スナップショットから復元したインスタンスをCDKで定義
database = rds.DatabaseInstanceFromSnapshot(self, "RestoredDatabase",
    snapshot_identifier="my-database-backup-20260120",
    engine=rds.DatabaseInstanceEngine.postgres(
        version=rds.PostgresEngineVersion.VER_17_5
    ),
    instance_type=ec2.InstanceType("t3.small"),
    vpc=vpc,
    security_groups=[db_security_group],
    credentials=rds.SnapshotCredentials.from_generated_secret("admin")
)
