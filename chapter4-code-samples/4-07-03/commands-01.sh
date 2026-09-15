# 1. ECRリポジトリを作成
cdk deploy ContainerRegistry

# 2. Dockerイメージをビルド・push
docker build -t my-app .
docker tag my-app:latest $REPOSITORY_URI:latest
docker push $REPOSITORY_URI:latest

# 3. ECSサービスをデプロイ
cdk deploy EcsService
