# 開発環境にデプロイ
cdk deploy --context env=dev --all

# または特定のStackのみ
cdk deploy MyApp-Database-Stack --context env=dev
