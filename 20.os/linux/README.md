# Ubuntu

アップデートを行うには、パッケージリストを更新して実行する

## パッケージリスト更新

```bash
sudo apt update -y
```

## 全てのパッケージを更新

```bash
sudo apt update -y
sudo apt upgrade -y
```

## セキュリティアップデートのみを実行

```bash
sudo apt install unattended-upgrades -y
```


# AlmaLinux

## パッケージリスト更新

```bash
sudo dnf update -y
```

## セキュリティアップデータの確認

```bash
sudo dnf check-update --security
```

## セキュリティアップデータのみ更新

```bash
sudo dnf update --security
```

## PODMANをインストール

```bash
sudo dnf install -y podman
```
