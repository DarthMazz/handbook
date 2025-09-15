

## GitLab 環境を構築する


### ディレクトリ作成

- ホストOS上にGitLab設定やデータを保持する場所を作成

```bash
sudo mkdir -p ~/gitlab/config ~/gitlab/data ~/gitlab/logs ~/gitlab/config/certs
```

### 自己署名証明書の作成

~/gitlab/config/certs ディレクトリで以下のコマンドを実行し、registry.gitlab.example.com のための証明書を作成します。

```bash
# openssl.cnf の作成
cat > openssl.cnf <<EOL
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = req_distinguished_name

[req_distinguished_name]
countryName = JP
stateOrProvinceName = Tokyo
localityName = Minato-ku
organizationName = Example Corporation
commonName = registry.gitlab.example.com

[req_ext]
subjectAltName = @alt_names

[alt_names]
DNS.1 = registry.gitlab.example.com
EOL

# 証明書の生成
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout registry.key -out registry.crt -config openssl.cnf
```

### docker-compose.yaml ファイル作成

```bash
cd gitlab
vi docker-compose.yml 
```

- docker-compose.yml

```yaml
version: '3.6'
services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    container_name: gitlab
    restart: always
    hostname: 'gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://gitlab.example.com'
        gitlab_rails['gitlab_shell_ssh_port'] = 2224
        gitlab_rails['registry_enabled'] = true
        gitlab_rails['registry_api_url'] = 'http://registry:5000'
        gitlab_rails['gitlab_registry_host'] = 'registry.gitlab.example.com'
        gitlab_rails['gitlab_registry_port'] = 443
    ports:
      - '80:80'
      - '2224:22'
    volumes:
      - './config:/etc/gitlab'
      - './logs:/var/log/gitlab'
      - './data:/var/opt/gitlab'
    networks:
      - gitlab-network

  registry:
    image: gitlab/gitlab-ce:latest
    container_name: registry
    restart: always
    hostname: 'registry.gitlab.example.com'
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        registry['enable'] = true
        registry['gitlab_uri'] = 'http://gitlab:80'
        registry['nginx_listen_port'] = 5000
        registry_nginx['listen_port'] = 5000
        registry_nginx['ssl_certificate'] = '/etc/gitlab/ssl/registry.crt'
        registry_nginx['ssl_certificate_key'] = '/etc/gitlab/ssl/registry.key'
    ports:
      - '443:443'
    volumes:
      - './config:/etc/gitlab'
      - './logs:/var/log/gitlab'
      - './data:/var/opt/gitlab'
      - './config/certs:/etc/gitlab/ssl:ro'
    networks:
      - gitlab-network

networks:
  gitlab-network:
    driver: bridge
```


## GitLab を起動する

```bash
docker compose up -d
```

## 外部PCでの設定

- 証明書のコピー:
GitLabサーバーで作成した証明書ファイル registry.crt を、何らかの方法（SCP、USBドライブなど）で外部PCにコピーします。

- registry.crt を /etc/docker/certs.d/registry.gitlab.example.com/ ディレクトリにコピーします。

### Dockerサービスを再起動

```bash
sudo mkdir -p /etc/docker/certs.d/registry.gitlab.example.com/
sudo cp /path/to/registry.crt /etc/docker/certs.d/registry.gitlab.example.com/
sudo systemctl restart docker
```

### ログイン

```bash
docker login registry.gitlab.example.com
```

### プッシュ

```bash
docker tag my-image registry.gitlab.example.com/my-project/my-image:latest
docker push registry.gitlab.example.com/my-project/my-image:latest
```

### プル

```bash
docker pull registry.gitlab.example.com/my-project/my-image:latest
```