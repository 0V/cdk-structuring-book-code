import aws_cdk as cdk
from cdk_nag import AwsSolutionsChecks

app = cdk.App()
# ... Stackの定義 ...

# cdk-nagのルールセットを追加
cdk.Aspects.of(app).add(AwsSolutionsChecks(verbose=True))
app.synth()
