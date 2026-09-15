# RDSスナップショットの作成
aws rds create-db-snapshot \
  --db-instance-identifier my-database \
  --db-snapshot-identifier my-database-backup-20260120
