# Poetryのインストール (pipを使用する場合)
pip install poetry

# 新規プロジェクトの初期化
poetry init

# 依存関係の追加
poetry add aws-cdk-lib constructs cdk-nag

# 開発用依存関係の追加
poetry add --group dev pytest black flake8 mypy

# 依存関係のインストール
poetry install

# 仮想環境内でコマンドを実行
poetry run cdk synth
poetry run black .

# 仮想環境のシェルに入る
poetry shell
