# git revert などでコードを戻したうえで、失敗したStackのみ再デプロイする
cdk deploy MyApp-Database-Stack --context env=prod

# 成功したStackは変更しない
