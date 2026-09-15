app = App()

# ネットワーク基盤 (初回構築後は滅多に変更しない)
infra = InfrastructureStack(app, "Infrastructure")

# データ層 (termination protectionで保護)
stateful = StatefulStack(app, "Stateful", vpc=infra.vpc)

# アプリケーション層 (リリースのたびにデプロイ)
application = ApplicationStack(app, "Application",
                               infra=infra,
                               stateful=stateful)

app.synth()

# デプロイコマンドの例
# 全Stackをデプロイ (初回)
# cdk deploy --all

# アプリケーションのみデプロイ (通常のリリース)
# cdk deploy Application
