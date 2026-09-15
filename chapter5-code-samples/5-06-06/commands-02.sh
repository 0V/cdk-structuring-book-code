# 既存Stackの更新に失敗した場合の出力例
❌  MyApp-prod failed: Error: The stack named MyApp-prod is in a failed state:
UPDATE_ROLLBACK_COMPLETE

# 原因を修正すれば、そのまま再デプロイできる
cdk deploy MyApp-prod --context env=prod
