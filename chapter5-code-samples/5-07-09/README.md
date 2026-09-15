# 5-07-09 デプロイ後の自動検証

| File | Kind | Validation | Source lines |
|---|---|---|---|
| `snippet-01.yml` | fragment | text-only | 2420-2454 |
| `commands-01.sh` | fragment | bash | 2464-2467 |
| `snippet-02.yml` | fragment | text-only | 2479-2497 |
| `snippet-03.yml` | fragment | text-only | 2505-2524 |

`Setup.sh` / `Setup.ps1` performs local static validation only. It never deploys or modifies AWS resources.
