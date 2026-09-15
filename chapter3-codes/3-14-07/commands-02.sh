# 仮想環境の再作成
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
