# ❌ 悪い例：依存関係が明示されていない
database_stack = DatabaseStack(app, "MyApp-Database")
app_stack = ApplicationStack(app, "MyApp-Application")

# アプリケーションStackがデータベースのエンドポイントを参照しようとするが、
# データベースStackがまだデプロイされていない可能性がある
