build:
	$(MAKE) -C locales/ru/LC_MESSAGES
	zip -r ../yandex-simple-bot.zip  . -x '*.git*'

deploy: build
	aws --endpoint-url=https://storage.yandexcloud.net s3 cp ../yandex-simple-bot.zip s3://notifyme/yandex-simple-bot.zip
	yc serverless function version create \
	--function-name=telegram-bot \
	--runtime python37 \
	--entrypoint main.handler \
	--memory 128m \
	--execution-timeout 60s \
	--package-bucket-name notifyme \
	--package-object-name yandex-simple-bot.zip \
	--environment TELEGRAM_BOT_API=${TELEGRAM_BOT_API} \
	--environment https_proxy=${PROXY}

locale: 
	@pygettext3 -d base -o locales/base.pot main.py
	@msgmerge -N locales/ru/LC_MESSAGES/base.po locales/base.pot >locales/ru/LC_MESSAGES/base.~po
	@mv locales/ru/LC_MESSAGES/base.~po locales/ru/LC_MESSAGES/base.po

deps:
	virtualenv -p python3.7 req
	req/bin/pip install -r requirements.txt

freeze:
	req/bin/pip freeze >requirements.txt
