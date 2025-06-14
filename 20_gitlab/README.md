# GitLab のインストール

## 環境

```bash
$ cat /etc/os-release
NAME="AlmaLinux"
VERSION="9.6 (Sage Margay)"
ID="almalinux"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.6"
PLATFORM_ID="platform:el9"
PRETTY_NAME="AlmaLinux 9.6 (Sage Margay)"
ANSI_COLOR="0;34"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:almalinux:almalinux:9::baseos"
HOME_URL="https://almalinux.org/"
DOCUMENTATION_URL="https://wiki.almalinux.org/"
BUG_REPORT_URL="https://bugs.almalinux.org/"

ALMALINUX_MANTISBT_PROJECT="AlmaLinux-9"
ALMALINUX_MANTISBT_PROJECT_VERSION="9.6"
REDHAT_SUPPORT_PRODUCT="AlmaLinux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.6"
SUPPORT_END=2032-06-01
```

```bash
$ docker --version
Docker version 28.2.2, build e6534b4
$ docker compose version
Docker Compose version v2.36.2
```


## docker インストール

```bash
sudo dnf install -y dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $(whoami)
```


## vi インストール

```bash
sudo dnf install vi -y
```


## GitLab 環境を構築する


### ディレクトリ作成

- ホストOS上にGitLab設定やデータを保持する場所を作成

```bash
sudo mkdir -p /srv/gitlab/config /srv/gitlab/logs /srv/gitlab/data
```


### docker-compose.yaml ファイル作成

```bash
mkdir container/gitlab
cd container/gitlab
vi docker-compose.yml 
```

- docker-compose.yml

```yaml
version: '3.8'
services:
  gitlab:
    image: 'gitlab/gitlab-ce:latest'
    container_name: gitlab
    hostname: 'gitlab.example.com' # ここをあなたのドメイン名またはIPアドレスに置き換えてください
    restart: always
    ports:
      - '80:80'
      - '443:443'
      - '22:22' # SSHポート。もしホストの22番ポートが使用中の場合は、'2222:22'のように変更してください
    volumes:
      - '/srv/gitlab/config:/etc/gitlab'
      - '/srv/gitlab/logs:/var/log/gitlab'
      - '/srv/gitlab/data:/var/opt/gitlab'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://gitlab.example.com' # ここもあなたのドメイン名またはIPアドレスに置き換えてください
        # 必要に応じて追加の設定をここに追加できます
        # 例: GitLabのメモリ制限
        # gitlab_rails['env'] = { 'RUBY_HEAP_ALLOC_MEMPROF' => '1', 'GITLAB_RAILS_MAX_MEM_MB' => '4096' }
    shm_size: '256m' # シェアメモリのサイズ。CI/CDのRunnerなどで必要になる場合があります。
```


## GitLab を起動する

```bash
docker compose up -d
```


## AlmaLinux側のファイアウォール設定

```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
```


## 初期パスワードを取得する

初期パスワードは、24時間のみ有効

```bash
sudo docker compose exec gitlab grep 'Password:' /etc/gitlab/initial_root_password
```


## ルートユーザでログイン

http://<GitLabのIPアドレス>にアクセスして ユーザ root 初期パスワードでログインする

Adminページから rootユーザパスワードを変更する



## Windows側からWSL2側へのポートフォーワード設定

```bash
netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=80 connectaddress=<WSL2のAlma LinuxのIPアドレス>
netsh interface portproxy add v4tov4 listenport=443 listenaddress=0.0.0.0 connectport=443 connectaddress=<WSL2のAlma LinuxのIPアドレス>
```
