# Docker

# 手順

## インストール (Ubuntu)

1. apt リポジトリを設定

```bash
# Add Docker's official GPG key:
sudo apt update -y
sudo apt upgrade -y
sudo apt install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y
```

2. Dockerパッケージをインストール

```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

```bash
$ docker --version
Docker version 28.4.0, build d8eb465
$ docker compose version
Docker Compose version v2.39.2
```

- 参考

    [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)


## sudo 無しで docker コマンドを利用する

```bash
sudo gpasswd -a <ユーザー名> docker
newgrp docker
```