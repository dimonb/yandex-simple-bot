build:
	zip -r ../yandex-simple-bot.zip  . -x '*.git*'

deploy: build
	aws --endpoint-url=https://storage.yandexcloud.net s3 cp ../yandex-simple-bot.zip s3://notifyme/yandex-simple-bot.zip
	yc serverless function version create \
	--function-name=telegram-bot \
	--runtime python37 \
	--entrypoint main.handler \
	--memory 128m \
	--execution-timeout 5s \
	--package-bucket-name notifyme \
	--package-object-name yandex-simple-bot.zip \
	--environment TELEGRAM_BOT_API=${TELEGRAM_BOT_API}