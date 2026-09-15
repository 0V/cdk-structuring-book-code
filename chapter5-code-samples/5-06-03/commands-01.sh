# 開発環境にデプロイ
cdk deploy --context env=dev

# ステージング環境にデプロイ
cdk deploy --context env=staging

# 本番環境にデプロイ（承認必須）
cdk deploy --context env=prod
