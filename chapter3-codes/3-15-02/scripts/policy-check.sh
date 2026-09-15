#!/bin/bash

# CDKテンプレートの生成
echo "Generating CDK templates..."
cdk synth --output cdk.out

# CloudFormation Guardによるチェック
echo "Running policy checks..."
cfn-guard validate \
    --rules organization-policies.guard \
    --data cdk.out/*.template.json \
    --show-summary all

# 結果の確認
if [ $? -eq 0 ]; then
    echo "All policy checks passed"
else
    echo "Policy violations found"
    exit 1
fi
