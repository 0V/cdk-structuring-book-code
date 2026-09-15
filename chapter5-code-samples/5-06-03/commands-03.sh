# 特定のStackのみデプロイ
cdk deploy MyApp-Database-Stack --context env=prod

# 複数のStackを順次デプロイ
cdk deploy MyApp-Network-Stack MyApp-Database-Stack --context env=prod

# すべてのStackをデプロイ
cdk deploy --all --context env=prod
