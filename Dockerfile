FROM python:slim

RUN useradd tracker

WORKDIR /home/tracker

COPY requirements.txt requirements.txt
COPY .env .env

RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY discord_bot.py intermediate.py reddit_bot.py boot.sh ./
RUN chmod +x boot.sh

RUN chown -R tracker:tracker ./
USER tracker

EXPOSE 80
ENTRYPOINT ["./boot.sh"]