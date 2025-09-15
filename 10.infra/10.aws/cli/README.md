# CLI

## Setup

- 新規インストール

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

- 更新インストール

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update
```


[AWS CLI の最新バージョンのインストールまたは更新](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html)

## Copy

```
aws s3 cp <ソースパス> <宛先パス> --recursive
```

```
aws s3 cp s3://ma2moto-bucket/unzipped/vscode-cosmosdb-main/vscode-cosmosdb-main/ s3://ma2moto-bucket/copied/vscode-cosmosdb-main/ --recursive
```

- プログレスバー非表示

```
aws s3 cp s3://ma2moto-bucket/unzipped/vscode-cosmosdb-main/vscode-cosmosdb-main/ s3://ma2moto-bucket/copied/vscode-cosmosdb-main/ --recursive --no-progress
```

- 非表示

```
aws s3 cp s3://ma2moto-bucket/unzipped/vscode-cosmosdb-main/vscode-cosmosdb-main/ s3://ma2moto-bucket/copied/vscode-cosmosdb-main/ --recursive --silent
```

```
aws s3 cp s3://ma2moto-bucket/unzipped/vscode-cosmosdb-main/vscode-cosmosdb-main/ s3://ma2moto-bucket/copied/vscode-cosmosdb-main/ --recursive > /dev/null 2>&1
```

## Delete

- 指定フォルダを削除

```
aws s3 rm s3://ma2moto-bucket/copied/ --recursive
```

- お試し削除（削除ファイルのリストアップ）

```
aws s3 rm s3://ma2moto-bucket/copied/ --recursive --dryrun
```

- 指定フォルダ削除（効率的な）

```
#!/bin/bash

BUCKET_NAME="your-bucket-name"
PREFIX_TO_DELETE="folder_to_delete/"

# オブジェクトのリストを取得し、削除リクエストのJSON形式に変換
aws s3api list-objects-v2 \
    --bucket "$BUCKET_NAME" \
    --prefix "$PREFIX_TO_DELETE" \
    --query 'Contents[].[Key]' \
    --output json | \
jq -c '{ Objects: .[] | { Key: .[0] } }' | \
while read -r line; do
    echo "Deleting objects: $line"
    aws s3api delete-objects \
        --bucket "$BUCKET_NAME" \
        --delete "$line"
done

echo "Deletion complete for prefix: $PREFIX_TO_delete"
```