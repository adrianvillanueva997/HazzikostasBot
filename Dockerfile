FROM python:3.8-alpine
WORKDIR /bot
COPY . .
RUN apk add --no-cache mariadb-dev mariadb-client build-base && pip3 install -r requirements.txt
CMD ["python3", "./bot.py"]
