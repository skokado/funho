# Funho

## デプロイ手順

### リポジトリクローン

```shell
$ git clone https://github.com/skokado/flask-template
$ mv flask-template funho
$ cd funho
```

### 設定ファイルの作成

- `config.py`

```shell
$ touch app/config.py
$ vi app/config.py
```

sample:

```python
import os

host=os.getenv('POSTGRES_HOST'),
user=os.getenv('POSTGRES_USER'),
password=os.getenv('POSTGRES_PASSWORD'),
database=os.getenv('POSTGRES_DB'),
SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}/{database}'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# セッション暗号化の秘密鍵.
SUPER_SECRET_KEY = 'secret_key_phrase'
# SUPER_SECRET_KEY = os.urandom(2048) # ランダム列にすると、ユーザはアプリ再起動の都度ログインが必要になる。
```

- `postgres.env`

```shell
$ touch postgres.env
$ vi postgres.env
```

sample:

```text
POSTGRES_HOST=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres
```

### コンテナビルド

```shell
$ docker volume create postgres_data
$ docker volume create flask_migrations
$ docker build . -t flask_app
$ docker-compose build
$ docker-compose up -d
```

### DBマイグレーション

```shell
$ docker exec -it app sh

flask db init
flask db migrate
flask db upgrade
psql -U postgres # ※データベーステーブルの確認
```