# 1. dockerhub でベースにしたいイメージを選択 (tensorflow, pytorch, ...)
FROM tensorflow/tensorflow:latest-gpu
# 2. メンテナラベルの付与 "dockerhub のアカウント名 <dockerhub に登録した e-mail>"
LABEL maintainer="nisk36 <nisknishimura@gmail.com>"

# 3. コンテナの作業場所の決定
ENV WORKSPACE /var/www
WORKDIR $WORKSPACE

# 4. Poerty のインストール
RUN pip install poetry
ENV PATH /root/.poetry/bin:$PATH

# 5. 2 つのライブラリ管理ファイルをコンテナにコピー (初めて環境構築する際は, ここはコメントアウト)
COPY pyproject.toml $WORKSPACE
COPY poetry.lock $WORKSPACE

# 6. Poetry でインストールできないライブラリをインストール (任意)
RUN pip install --ignore-installed gym
RUN pip install --ignore-installed keras
RUN pip install --ignore-installed keras-rl
RUN pip install --ignore-installed keras-rl2
RUN pip install --ignore-installed tensorflow
RUN pip install --ignore-installed matplotlib
RUN pip install --ignore-installed numpy
RUN pip install --ignore-installed pydot
#RUN pip install --ignore-installed random

# 7. Poetry によるライブラリの依存関係の解決 (初めて環境構築する際は, ここはコメントアウト)#
RUN poetry config virtualenvs.create false && \
    pip install --upgrade pip && \
    pip install -U setuptools && \
    poetry install -n

# 8. エントリーポイントの指定
CMD ["python"]