# 1. 既存リソースの情報を収集
aws ec2 describe-vpcs --vpc-ids vpc-12345678
aws rds describe-db-instances --db-instance-identifier existing-db

# 2. 新しい環境で CDK Stack を作成
cdk deploy NewStack --context environment=new

# 3. アプリケーションの接続先を新しいリソースに変更
# （アプリケーション設定ファイルやEnvironment変数を更新）

# 4. 動作確認後、古いリソースを削除（DBは最終スナップショットを必ず取得する）
aws rds delete-db-instance \
  --db-instance-identifier existing-db \
  --final-db-snapshot-identifier existing-db-final-snapshot
aws ec2 delete-vpc --vpc-id vpc-12345678
