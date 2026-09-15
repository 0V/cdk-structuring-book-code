# ✅ 良い例：依存関係を明示的に定義
database_stack = DatabaseStack(app, "MyApp-Database")
app_stack = ApplicationStack(app, "MyApp-Application",
    database_endpoint=database_stack.database.db_instance_endpoint_address
)

# CDKが自動的に依存関係を解決し、正しい順序でデプロイする
app_stack.add_dependency(database_stack)
