# 仮想環境の作成
python -m venv .venv

# 仮想環境の有効化 (macOS/Linux)
source .venv/bin/activate

# Windowsの場合はGit Bashを使用し、以下のコマンドを実行
source .venv/Scripts/activate

# CDKと必要なライブラリのインストール
pip install aws-cdk-lib constructs
pip install -r requirements.txt

# 依存関係の固定
pip freeze > requirements-lock.txt
