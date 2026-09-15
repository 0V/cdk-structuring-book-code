# import順序のチェック
$ isort --check-only sample_code.py
ERROR: sample_code.py Imports are incorrectly sorted and/or formatted.

# 実際に整理を実行
$ isort sample_code.py
Fixing sample_code.py

# 整理後の確認
$ isort --check-only sample_code.py
(何も出力されなければOK)
