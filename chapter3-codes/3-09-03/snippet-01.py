# 複数ルールセットの例
if app.node.try_get_context("environment") == "production":
    # 本番環境では厳しいチェックを適用
    cdk.Aspects.of(app).add(AwsSolutionsChecks(verbose=True))
    cdk.Aspects.of(app).add(NIST80053R5Checks(verbose=True))
else:
    # 開発環境では基本的なチェックのみ
    cdk.Aspects.of(app).add(AwsSolutionsChecks(verbose=True))
