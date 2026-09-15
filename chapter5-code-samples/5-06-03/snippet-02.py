# 東京リージョン向けのStack
MyStack(app, "MyApp-prod-tokyo",
    env=Environment(account="123456789012", region="ap-northeast-1"),
    config=config
)

# 大阪リージョン向けのStack
MyStack(app, "MyApp-prod-osaka",
    env=Environment(account="123456789012", region="ap-northeast-3"),
    config=config
)
