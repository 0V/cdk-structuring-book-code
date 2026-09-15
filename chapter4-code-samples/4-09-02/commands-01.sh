# 1. CDKプロジェクトの初期化
cdk init app --language python

# 2. 依存関係のインストール
pip install -r requirements.txt

# 3. CloudFormationテンプレートの生成と確認
cdk synth

# 4. 初回デプロイ（ブートストラップが必要な場合）
cdk bootstrap

# 5. Stackのデプロイ
cdk deploy

# 6. デプロイ状況の確認
aws cloudformation describe-stacks --stack-name YourStackName
