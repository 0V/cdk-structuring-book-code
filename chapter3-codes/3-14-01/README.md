# 3-14-01 比較用の開発環境

第3章で構築した環境との違いを確認するための、独立して動作するCDKプロジェクトです。

- Python 3.13
- 最大行長100文字
- `aws-cdk-lib>=2.170.0,<3.0.0`
- Black 24以上、Flake8 7以上
- Mypy strictモード
- isortを含むPre-commit設定

## セットアップ

Linux / macOS:

```bash
./Setup.sh
```

Windows PowerShell:

```powershell
.\Setup.ps1
```

セットアップは依存導入、コード品質検査、単体テスト、`cdk synth`までを実行します。AWSへのデプロイは行いません。
