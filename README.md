# CDK実践 サンプルコード

書籍「AWS CDK実践ガイド─クラウドインフラをコードで構造化する」で使っているサンプルコードです。

## 収録内容

| ディレクトリ | 対応する章 | 内容 |
|---|---|---|
| [`chapter2-handson/`](chapter2-handson/) | 第2章 | 節ごとのCDKプロジェクト |
| [`chapter3-codes/`](chapter3-codes/) | 第3章 | 開発環境や品質チェックの設定例 |
| [`chapter4-code-samples/`](chapter4-code-samples/) | 第4章 | システムを分割・構造化するコード例 |
| [`chapter5-code-samples/`](chapter5-code-samples/) | 第5章 | リリースやCI/CDのコード例 |
| [`links/`](links/) | 全章 | 本文で紹介したリンク |

第2章は、読み進めた時点のコードを節ごとに残しています。そのため、同じファイルが複数のディレクトリに入っています。
第3章以降の`snippet-*`、`commands-*`、`output-*`は、本文中の抜粋やコマンド例、出力例です。

## 動かし方

Python 3.12、Node.js 22または24、AWS CDK CLI v2を用意してください。`chapter3-codes/3-14-01`だけはPython 3.13を使います。

各サンプルのディレクトリにあるREADMEを確認し、LinuxまたはmacOSでは`Setup.sh`、Windowsでは`Setup.ps1`を実行します。

```bash
cd chapter2-handson/2-03-03
./Setup.sh
```

```powershell
cd chapter2-handson\2-03-03
.\Setup.ps1
```

Setupスクリプトは、必要なライブラリのインストール、テスト、CDKの合成までを行います。AWSへのデプロイやリソースの削除は行いません。

## 本文で紹介したリンク

本文に出てくる公式ドキュメントや関連ツールは、[`links/README.md`](links/README.md)に章ごとにまとめています。

## AWSへデプロイする場合

`cdk deploy`を実行するとAWSリソースが作成され、料金が発生する場合があります。実行前に`cdk diff`で変更内容を確認してください。検証後は不要なリソースが残っていないことも確認してください。
