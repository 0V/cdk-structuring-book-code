# 新規Stackの作成に失敗した場合の出力例
❌  MyApp-prod failed: Error: The stack named MyApp-prod failed creation,
it may need to be manually deleted from the AWS console:
ROLLBACK_COMPLETE

# 失敗したStackを削除してから、原因を修正して再デプロイする
cdk destroy MyApp-prod --context env=prod
cdk deploy MyApp-prod --context env=prod
