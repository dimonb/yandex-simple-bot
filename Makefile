build:
	zip -r ../yandex-simple-bot.zip  . -x '*.git*'

deploy: build
	yc serverless function version create \
	--function-name=telegram-bot \
	--runtime python37 \
	--entrypoint main.handler \
	--memory 128m \
	--execution-timeout 5s \
	--source-path ../yandex-simple-bot.zip
