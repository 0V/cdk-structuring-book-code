# 手動デプロイでのロールバック
$ cdk deploy --context env=prod
# デプロイ失敗に気づく

$ git revert HEAD
$ cdk deploy --context env=prod
