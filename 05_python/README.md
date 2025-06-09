# Python

## Setup

- rye

```
curl -sSf https://rye.astral.sh/get | bash
```

- プロジェクトを初期化する

```
rye init
```

```
rye init <Project Name>
```

## SampleCode

### TaskGroup

```bash
pip install aioboto3
```

```python
import asyncio
import aioboto3
import os
import math # 分割計算のために使用

async def download_s3_object_aioboto3(s3_client, bucket_name, object_key, local_path):
    """S3からファイルをダウンロードする非同期関数 (aioboto3を使用)"""
    print(f"Downloading {object_key} to {local_path}...")
    try:
        await s3_client.download_file(bucket_name, object_key, local_path)
        print(f"Successfully downloaded {object_key}")
    except Exception as e:
        print(f"Error downloading {object_key}: {e}")
        # TaskGroupで捕捉できるように例外を再発生させる
        raise

async def main():
    bucket_name = 'your-bucket-name' # 実際のS3バケット名に置き換えてください

    # 仮のオブジェクトキーリスト（合計10個）
    all_object_keys = [f'file_{i:02d}.txt' for i in range(1, 11)]

    download_dir = 'downloads_aioboto3_batched'
    os.makedirs(download_dir, exist_ok=True)

    # ダウンロードを何回に分けるか
    num_batches = 3

    # 1バッチあたりのファイル数を計算
    # 例: 10ファイルを3バッチで分割すると、4, 3, 3 となる
    batch_size = math.ceil(len(all_object_keys) / num_batches) # 切り上げ

    session = aioboto3.Session()

    async with session.client('s3') as s3_client:
        print("Starting batched downloads with TaskGroup and aioboto3...")

        for i in range(num_batches):
            # 現在のバッチでダウンロードするファイルの範囲を決定
            start_index = i * batch_size
            end_index = min((i + 1) * batch_size, len(all_object_keys))
            current_batch_keys = all_object_keys[start_index:end_index]

            if not current_batch_keys:
                break # ダウンロードするファイルがない場合はループを抜ける

            print(f"\n--- Starting Batch {i + 1}/{num_batches} (Files: {', '.join(current_batch_keys)}) ---")

            try:
                async with asyncio.TaskGroup() as tg:
                    for key in current_batch_keys:
                        local_path = os.path.join(download_dir, os.path.basename(key))
                        tg.create_task(download_s3_object_aioboto3(s3_client, bucket_name, key, local_path))
            except Exception as eg:
                print(f"\nOne or more tasks failed in Batch {i + 1}: {eg}")
                for e in eg.exceptions:
                    print(f"  - {type(e).__name__}: {e}")
            finally:
                print(f"--- Batch {i + 1} completed. ---")

    print("\nAll batched download tasks initiated and processed.")

if __name__ == "__main__":
    # 実行前に、'your-bucket-name' と all_object_keys を実際のS3バケットとオブジェクトに置き換えてください。
    # また、AWS認証情報が設定されていることを確認してください（例: 環境変数 AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY など）。
    asyncio.run(main())
```
