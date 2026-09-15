# 本番環境への変更内容を確認
cdk diff --context env=prod

# 特定のStackのみ確認
cdk diff MyApp-Database-Stack --context env=prod
