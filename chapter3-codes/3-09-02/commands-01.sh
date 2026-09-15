# cdk synthを実行するとcdk-nagのチェックも実行される
$ cdk synth

# 検証結果例:
# [Error at /DemoStack/DemoBucket/Resource] AwsSolutions-S1: The S3 Bucket has server access logs disabled. The bucket should have serve access logging enabled to provide detailed records for the requests the are made to the bucket. ...
