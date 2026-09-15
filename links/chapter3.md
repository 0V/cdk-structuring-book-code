# 第3章 開発者環境の整備

- [データ所在地付きGitHub Enterprise Cloudについて](https://docs.github.com/ja/enterprise-cloud@latest/admin/data-residency/about-github-enterprise-cloud-with-data-residency)
- [AWS Well-Architected Framework セキュリティの柱](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [AWS CDK Aspects](https://docs.aws.amazon.com/cdk/v2/guide/aspects.html)
- [pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)
- [Black](https://github.com/psf/black)
- [Flake8](https://github.com/pycqa/flake8)
- [detect-secrets](https://github.com/Yelp/detect-secrets)
- [第3章の比較用サンプルコード](https://github.com/0V/cdk-structuring-book-code/tree/main/chapter3-codes/3-14-01)
- [本書の公開サンプルコードリポジトリ](https://github.com/0V/cdk-structuring-book-code.git)
- [CloudFormation Guard](https://docs.aws.amazon.com/ja_jp/cfn-guard/latest/ug/what-is-guard.html)

CloudFormation GuardをLinuxへインストールする場合は、次のコマンドを実行します。

```bash
curl -L https://github.com/aws-cloudformation/cloudformation-guard/releases/latest/download/cfn-guard-v3-ubuntu-latest.tar.gz | tar xz
sudo mv cfn-guard /usr/local/bin/
```
