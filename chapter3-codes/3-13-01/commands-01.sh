# Blackによるフォーマットチェック (変更なしで終了すればOK)
black --check .

# Flake8によるLintチェック
flake8 .

# Mypyによる型チェック
mypy .

# isortによるimport順チェック
isort --check-only .
