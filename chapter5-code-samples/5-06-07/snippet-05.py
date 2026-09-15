# ❌ 悪い例：RemovalPolicyが設定されていない
database = rds.DatabaseInstance(self, "Database",
    # RemovalPolicyが設定されていないため、
    # Stackを削除するとデータベースも削除される
)
