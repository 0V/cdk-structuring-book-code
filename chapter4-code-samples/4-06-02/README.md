# 4-06-02 環境別設計パターン

| File | Kind | Validation | Source lines |
|---|---|---|---|
| `snippet-01.py` | fragment | python-ast | 1412-1445 |
| `configs/development.json` | complete-file | json | 1455-1462 |
| `configs/production.json` | complete-file | json | 1466-1473 |
| `snippet-02.py` | fragment | python-ast | 1477-1485 |
| `commands-01.sh` | fragment | bash | 1491-1495 |

`Setup.sh` / `Setup.ps1` performs local static validation only. It never deploys or modifies AWS resources.
