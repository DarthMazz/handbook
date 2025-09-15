# GitLab のインストール


## 環境


- os バージョン

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

- カーネルバージョン

```bash
$ cat /proc/version
Linux version 5.15.167.4-microsoft-standard-WSL2 (root@f9c826d3017f) (gcc (GCC) 11.2.0, GNU ld (GNU Binutils) 2.37) #1 SMP Tue Nov 5 00:21:55 UTC 2024
```

- docker バージョン

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

- usermod を適用するために一度シェルを再起動する


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
mkdir -p container/gitlab
cd container/gitlab
vi docker-compose.yml 
```

- docker-compose.yml

```yaml
version: '3.8'
services:
  gitlab:
    image: 'gitlab/gitlab-ce:17.8.7-ce.0'
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

- docker-compose.yml

container registryを起動する場合

```yaml
version: '3.8'
services:
  gitlab:
    image: 'gitlab/gitlab-ce:18.2.1-ce.0' # 指定されたバージョン
    container_name: gitlab
    hostname: gitlab.local # コンテナ内部のホスト名
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        # GitLabの外部URL (MacのDocker Desktopの場合、localhostを使用)
        external_url 'http://localhost:18081' # GitLab Web UIへのアクセスポートを18081にする

        gitlab_rails['gitlab_shell_ssh_port'] = 2222 # SSHポート（任意）

        # Container Registryの設定 (HTTPアクセス)
        # registry_external_urlは、Container RegistryにアクセスするためのURLです。
        # MacのDocker Desktopの場合、localhostを使用し、異なるポートを割り当てます。
        registry_external_url 'http://localhost:5005'
        gitlab_rails['registry_enabled'] = true
        gitlab_rails['registry_host'] = 'localhost' # レジストリのホスト名
        gitlab_rails['registry_port'] = 5005 # レジストリのポート

        # HTTPアクセスなのでSSL/Let's Encrypt関連はすべて無効化または削除
        nginx['listen_port'] = 80 # GitLab NginxがHTTPリクエストを待ち受けるポート
        nginx['listen_https'] = false # HTTPSを無効化
        nginx['redirect_http_to_https'] = false # HTTPからHTTPSへのリダイレクトを無効化

        # registry_nginxに関するHTTPS設定も同様に無効化
        registry_nginx['listen_port'] = 5005 # レジストリNginxがHTTPリクエストを待ち受けるポート
        registry_nginx['listen_https'] = false # HTTPSを無効化
        registry_nginx['redirect_http_to_https'] = false # HTTPからHTTPSへのリダイレクトを無効化

        # Container Registryのストレージ設定（デフォルトはローカルファイルシステム）
        # registry['storage']['filesystem']['path'] = "/var/opt/gitlab/gitlab-rails/shared/registry" # デフォルト

    ports:
      - '18081:80' # GitLab Web UIへのアクセスポートを18081にマッピング
      - '5005:5005' # Container Registryへのアクセスポートを5000にマッピング
      - '2222:22' # SSHポートをマッピング
    volumes:
      - './config:/etc/gitlab'
      - './logs:/var/log/gitlab'
      - './data:/var/opt/gitlab'
    shm_size: '256m'
    restart: always
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
docker compose exec gitlab grep 'Password:' /etc/gitlab/initial_root_password
```


## ルートユーザでログイン

http://<GitLabのIPアドレス>にアクセスして ユーザ root 初期パスワードでログインする

Adminページから rootユーザパスワードを変更する


## Windows側からWSL2側へのポートフォーワード設定

```bash
netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=80 connectaddress=<WSL2のAlma LinuxのIPアドレス>
netsh interface portproxy add v4tov4 listenport=443 listenaddress=0.0.0.0 connectport=443 connectaddress=<WSL2のAlma LinuxのIPアドレス>
```


# GitLab Runnerのインストール


### ディレクトリ作成

- ホストOS上にGitLab Runner設定を保持する場所を作成

```bash
sudo mkdir -p /srv/gitlab-runner/config
```


### docker-compose.yaml ファイル作成

```bash
cd
mkdir container/gitlab-runner
cd container/gitlab-runner
vi docker-compose.yml 
```

- docker-compose.yml

```yaml
version: '3.8'
services:
  gitlab-runner:
    image: gitlab/gitlab-runner:alpine-v17.8.5 # 最新の安定版を使用することを推奨します
    restart: always
    container_name: gitlab-runner
    volumes:
      - /srv/gitlab-runner/config:/etc/gitlab-runner # 設定ファイルをホストに永続化
      - /var/run/docker.sock:/var/run/docker.sock # Docker-in-Docker (dind) を使用する場合に必要
    environment:
      # DinD (Docker in Docker) を有効にするための設定
      DOCKER_DRIVER: overlay2
      DOCKER_TLS_CERTDIR: "" # DinD で TLS を無効化（テスト環境向け）
```


## GitLab-Runner を起動する

```bash
docker compose up -d
```


## GitLab-Runner の登録


### 登録トークンと GitLab URLをメモする

- GitLab にログインし、プロジェクトまたはグループの設定から「CI/CD」->「Runners」に移動します。

- 「Register an instance runner」または「New project runner」をクリックし、登録トークンと GitLab URL をメモします。


### GitLab-Runnerを GitLabに登録する

```bash
docker compose exec gitlab-runner gitlab-runner register
```

- プロンプトが表示されたら、以下の情報を入力します。
* Please enter the GitLab instance URL: ここに、メモした GitLab の URL (例: http://your-gitlab-hostname) を入力します。
* Please enter the registration token: ここに、メモした登録トークンを入力します。
* Please enter a description for the runner: ランナーの説明 (例: My Docker Runner on WSL2)
* Please enter tags for the runner (comma-separated): ランナーに割り当てるタグ (例: docker, wsl2, dind)。CI/CD パイプラインでこのタグを使用して特定のランナーを呼び出します。
* Please enter an executor: docker と入力します。
* Please enter the default Docker image (e.g. ruby:2.7): デフォルトの Docker イメージ (例: alpine:latest または ubuntu:latest)。これは gitlab-ci.yml で指定がない場合に利用されます。
* Please enter the Docker 'pull policy': always を推奨します。
* Please enter the Docker 'privileged' mode (true/false): DinD を有効にするため、true と入力します。セキュリティリスクを理解して設定してください。
* Please enter the Docker 'disable cache' mode (true/false): お好みで。
* Please enter the Docker 'volumes': ここに DinD 用のボリュームを追加します。"/certs/client" と入力し、Enter キーを押した後、何も入力せずに再度 Enter キーを押して終了します。

- config/confit.toml

```
concurrent = 1
check_interval = 0
shutdown_timeout = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "My Docker Runner"
  url = "http://172.23.9.230/"
  id = 3
  token = "glrt-t3_cG94Fid6A8gbJS-ywtB9"
  token_obtained_at = 2025-06-21T07:55:18Z
  token_expires_at = 0001-01-01T00:00:00Z
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    MaxUploadedArchiveSize = 0
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "alpine:latest"
    privileged = true
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/certs/client"]
    shm_size = 0
    network_mtu = 0
```


## GitLab-Runner の動作確認


### .gitlab-ci.yml の作成

- プロジェクトルートに.gitlab-ci.yml を作成する

```yaml
image: docker:28.2.2-dind-alpine3.22

stages:
  - build

build_image:
  stage: build
  tags:
    - test-runner
  script:
    - docker info
    - docker build -t my-dind-image .
    - docker images
  variables:
    DOCKER_HOST: tcp://docker:2375 # DinD 用の設定
    DOCKER_TLS_CERTDIR: ""        # DinD 用の設定
  services:
    - docker:28.2.2-dind-alpine3.22 # GitLab Runner内でDockerデーモンをサービスとして起動
```


### Dockerfileを作成する

- Dockerfile

```
FROM alpine:latest
CMD echo "Hello from DinD!"
```