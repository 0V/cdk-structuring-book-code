# 第2章 ハンズオン

書籍の第2章を節ごとに切り出した独立スナップショットです。ディレクトリ名は書籍の章・節・小節に対応します。

各ディレクトリでLinux / macOSは`./Setup.sh`、Windowsは`.\Setup.ps1`を実行すると、依存導入、単体テスト、CDK合成まで実行します。AWSへのデプロイは行いません。

| Directory | Section | Validation |
|---|---|---|
| [`2-03-03`](2-03-03/) | CDKプロジェクトの初期化 | `pytest` / `cdk synth` |
| [`2-03-04`](2-03-04/) | 最初のStackを作成する | `pytest` / `cdk synth` |
| [`2-03-08`](2-03-08/) | Lambda関数の追加と差分確認 | `pytest` / `cdk synth` |
| [`2-03-09`](2-03-09/) | API Gatewayの追加と動作確認 | `pytest` / `cdk synth` |
| [`2-04-02`](2-04-02/) | 統計取得用Lambda関数の追加 | `pytest` / `cdk synth` |
| [`2-04-03`](2-04-03/) | プロジェクト構造の整理とConstruct | `pytest` / `cdk synth` |
| [`2-04-04`](2-04-04/) | ConstructをStackへ組み込む | `pytest` / `cdk synth` |
| [`2-04-05`](2-04-05/) | Appで新旧Stackを並行して定義する | `pytest` / `cdk synth` |
| [`2-04-06`](2-04-06/) | 新構成の検証と切り替え | `pytest` / `cdk synth` |
| [`2-05-01`](2-05-01/) | L1 Construct: CloudFormationの直接マッピング | `pytest` / `cdk synth` |
| [`2-05-03`](2-05-03/) | L2 Construct: 便利機能付きの高レベルAPI (推奨) | `pytest` / `cdk synth` |
| [`2-06-03`](2-06-03/) | Fn::ImportValueとExportによる値の受け渡し | `pytest` / `cdk synth` |
| [`2-06-04`](2-06-04/) | クロスStack参照による直接参照 | `pytest` / `cdk synth` |
| [`2-06-05`](2-06-05/) | 環境変数とSSMパラメータを活用した疎結合 | `pytest` / `cdk synth` |
| [`2-09-02`](2-09-02/) | 訪問者カウンターアプリでのエスケープハッチ活用 | `pytest` / `cdk synth` |
| [`2-10-02`](2-10-02/) | 実践的な活用例: DynamoDBバックアップカスタムリソース | `pytest` / `cdk synth` |
