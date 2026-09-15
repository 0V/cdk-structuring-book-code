app = App()

# 基盤Stack
network = NetworkStack(app, "Network")

# データStack（基盤に依存）
data = DataStack(app, "Data", vpc=network.vpc)

# アプリケーションStack（基盤とデータに依存）
application = ApplicationStack(app, "Application",
                              vpc=network.vpc,
                              database=data.database)

app.synth()
