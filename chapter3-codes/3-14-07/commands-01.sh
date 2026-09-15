# 仮想環境が有効化されている場合は先に無効化
deactivate

# 仮想環境の削除
rm -rf .venv

# 削除されたことを確認
ls -la .venv
# 出力例: ls: .venv: No such file or directory
