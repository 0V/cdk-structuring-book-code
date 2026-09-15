# 本番環境への変更内容を確認
cdk diff --context env=prod

# 出力例
Stack MyApp-prod
Resources
[+] AWS::EC2::SecurityGroup MySecurityGroup MySecurityGroupABC123
[~] AWS::RDS::DBInstance MyDatabase MyDatabaseDEF456
 └─ [~] DBInstanceClass
     ├─ [-] db.t3.micro
     └─ [+] db.t3.small
[±] AWS::Lambda::Function MyFunction MyFunctionGHI789 (replacement)
[-] AWS::S3::Bucket OldBucket OldBucketJKL012
