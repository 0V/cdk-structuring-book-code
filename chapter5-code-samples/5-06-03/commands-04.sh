# 依存関係を考慮した順次デプロイ
cdk deploy MyApp-Network-Stack --context env=prod
cdk deploy MyApp-Database-Stack --context env=prod
cdk deploy MyApp-Application-Stack --context env=prod
