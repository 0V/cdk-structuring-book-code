# 手動デプロイ後のヘルスチェック
$ cdk deploy --context env=prod
$ curl https://api.example.com/health
{"status":"healthy"}
