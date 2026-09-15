# 5-07-05 環境別のパイプライン設計

| File | Kind | Validation | Source lines |
|---|---|---|---|
| `.github/workflows/deploy.yml` | complete-file | text-only | 1885-1934 |
| `.github/workflows/deploy-with-environments.yml` | complete-file | text-only | 1946-2028 |

`Setup.sh` / `Setup.ps1` performs local static validation only. It never deploys or modifies AWS resources.
