# ロールバックを継続する
aws cloudformation continue-update-rollback \
  --stack-name MyApp-prod

# 特定のリソースのロールバックをスキップして継続する
aws cloudformation continue-update-rollback \
  --stack-name MyApp-prod \
  --resources-to-skip MyDatabase
