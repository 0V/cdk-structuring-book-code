# Lambda関数のログを確認
aws logs tail /aws/lambda/my-function --follow

# ECSタスクのログを確認
aws logs tail /ecs/my-service --follow
