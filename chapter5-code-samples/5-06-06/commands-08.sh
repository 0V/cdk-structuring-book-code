# DynamoDBテーブルを特定の時点に復元
aws dynamodb restore-table-to-point-in-time \
  --source-table-name my-table \
  --target-table-name my-table-restored \
  --restore-date-time 2026-01-20T10:00:00Z
