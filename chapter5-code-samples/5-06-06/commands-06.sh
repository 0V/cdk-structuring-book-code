# RDSスナップショットから新しいインスタンスを作成
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier my-database-restored \
  --db-snapshot-identifier my-database-backup-20260120 \
  --db-subnet-group-name my-app-db-subnet-group \
  --vpc-security-group-ids sg-0123456789abcdef0

# 復元が完了したら、アプリケーションの接続先を変更
