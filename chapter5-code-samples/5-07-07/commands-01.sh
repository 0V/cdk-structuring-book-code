# 手動デプロイでのdiff確認
$ cdk diff --context env=prod

Stack MyApp-prod
Resources
[~] AWS::RDS::DBInstance MyDatabase
 └─ [~] DBInstanceClass
     ├─ [-] db.t3.micro
     └─ [+] db.t3.small
