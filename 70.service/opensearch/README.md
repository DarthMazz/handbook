# OpenSearch

# 環境

```bash
$ cat /etc/os-release 
PRETTY_NAME="Ubuntu 24.04.3 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.3 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=noble
LOGO=ubuntu-logo

$ docker --version
Docker version 28.4.0, build d8eb465
$ docker compose version
Docker Compose version v2.39.2
```

# 手順

## インストール (OpenSearch)

1. Dockerネットワーク作成

```bash
sudo docker network create opensearch-net
```

```bash
$ sudo docker network ls
NETWORK ID     NAME             DRIVER    SCOPE
a72d39d2d7c4   bridge           bridge    local
fa88e6c44eb3   host             host      local
74dcaad6db71   none             null      local
7bbe632ab7c6   opensearch-net   bridge    local
```

2. docker-compose.ymlを作成する

```yaml
services:
  opensearch-node1:
    image: opensearchproject/opensearch:3.2.0
    container_name: opensearch-node1
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node1
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD}  # 最低8文字, 大文字, 小文字, 数字, 記号の全てを含む必要あり
    volumes:
      - opensearch-data:/usr/share/opensearch/data
    ports:
      - "9200:9200"
      - "9600:9600"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    networks:
      - opensearch-net

volumes:
  opensearch-data:

networks:
  opensearch-net:
    external: true  # 既存のネットワークを使用する
```

3. 初期パスワードを環境変数に設定する

```bash
export OPENSEARCH_INITIAL_ADMIN_PASSWORD=<password>
```

4. 起動

```bash
sudo docker compose up -d
```

5. 起動確認

```bash
$ curl -XGET https://localhost:9200 -ku admin:${OPENSEARCH_INITIAL_ADMIN_PASSWORD}

{
  "name" : "opensearch-node1",
  "cluster_name" : "opensearch-cluster",
  "cluster_uuid" : "CZb3_blwTFShvLiMuU1OeA",
  "version" : {
    "distribution" : "opensearch",
    "number" : "3.2.0",
    "build_type" : "tar",
    "build_hash" : "6adc0bf476e1624190564d7fbe4aba00ccf49ad8",
    "build_date" : "2025-08-12T03:55:01.226522683Z",
    "build_snapshot" : false,
    "lucene_version" : "10.2.2",
    "minimum_wire_compatibility_version" : "2.19.0",
    "minimum_index_compatibility_version" : "2.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```