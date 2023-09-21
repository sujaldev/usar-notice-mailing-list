FROM debian:latest

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install python3 python3-pip -y

RUN rm /usr/lib/python3*/EXTERNALLY-MANAGED \
    && useradd -m mailer \
    && mkdir -p /app/data \
    && chown -R mailer:mailer /app

USER mailer
WORKDIR /app
COPY --chown=mailer requirements.txt .
RUN pip3 install -Ur requirements.txt

COPY --chown=mailer ./src/*.py .

CMD ["python3", "main.py"]