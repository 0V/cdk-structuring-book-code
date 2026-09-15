# 4-07-03 コメントアウトしないとデプロイできないリソース

| File | Kind | Validation | Source lines |
|---|---|---|---|
| `snippet-01.py` | fragment | python-ast | 1568-1584 |
| `snippet-02.py` | fragment | python-ast | 1592-1605 |
| `snippet-03.py` | fragment | python-ast | 1613-1634 |
| `commands-01.sh` | fragment | bash | 1640-1649 |

`Setup.sh` / `Setup.ps1` performs local static validation only. It never deploys or modifies AWS resources.
