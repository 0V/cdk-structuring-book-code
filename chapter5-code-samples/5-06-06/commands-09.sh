# S3オブジェクトの以前のバージョンを復元
aws s3api list-object-versions \
  --bucket my-bucket \
  --prefix my-file.txt

# 特定のバージョンを復元
aws s3api copy-object \
  --bucket my-bucket \
  --copy-source my-bucket/my-file.txt?versionId=<version-id> \
  --key my-file.txt
