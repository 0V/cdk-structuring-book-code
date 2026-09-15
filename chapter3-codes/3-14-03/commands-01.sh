# Python 3.13で仮想環境を作成 (プロジェクトの要件に合わせる)
python3.13 -m venv .venv

# 仮想環境の有効化 (macOS/Linux)
source .venv/bin/activate
# Windowsの場合: source .venv/Scripts/activate

# 依存関係のインストール
pip install -r requirements-dev.txt

# Pre-commitフックの有効化
pre-commit install
