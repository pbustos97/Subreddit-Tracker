FROM alpine:latest

ENV USER=tracker
ENV UID=38403
ENV GID=48305

RUN apk --no-cache add gcc musl-dev python3 python3-dev curl
RUN addgroup -S tracker
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "$USER" \
    --no-create-home \
    --uid "$UID" \
    "$USER"

WORKDIR /home/tracker

COPY requirements.txt requirements.txt
COPY .env .env

RUN python3 -m venv venv
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY discord_bot.py intermediate.py reddit_bot.py boot.sh ./
RUN chmod +x boot.sh

RUN chown -R tracker:tracker ./
USER tracker

EXPOSE 80
CMD venv/bin/python intermediate.py