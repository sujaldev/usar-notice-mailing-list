FROM debian:latest

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install python3 python3-pip -y

RUN rm /usr/lib/python3*/EXTERNALLY-MANAGED && mkdir -p /app/data

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -Ur requirements.txt
COPY ./src/*.py .

CMD ["python3", "main.py"]