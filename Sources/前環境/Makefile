
# 命名規則 : (dockerhub のアカウント名)/(環境名):(バージョンタグ)
IMAGE_NAME := card_game_env:1.0
# 命名規則 : (環境名).(使用者の名前)
CONTAINER_NAME := card_game_env.nishimura

# サーバに IMAGE_NAME という名前の Docker イメージが作られる.
.PHONY: build
build:
	@docker build . -t $(IMAGE_NAME)

# IMAGE_NAME というイメージを元に CONTAINER_NAME という名前の Docker コンテナが起動する.
.PHONY: run
run:
	@docker run --rm -it \
          --gpus all \
          -u root \
          --name $(CONTAINER_NAME) \
          -v $(shell pwd):/var/www \
          $(IMAGE_NAME) bash