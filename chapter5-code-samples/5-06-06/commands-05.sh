# 問題のあるcommitの変更を打ち消すcommitを作成する
git revert <commit-hash>

# 再デプロイ
cdk deploy --context env=prod
