FROM python:3.10-slim
LABEL description="Python 3.10 multi architecture image for testing and development of Service Based Architecture for Distributed Systems"
LABEL maintainer="Vinicius Werlich Kuci Barbosa <vinicius.kuci@hotmail.com>"

WORKDIR /T-Rex
COPY requirements.txt .
#COPY . .

RUN apt-get update && apt-get install -y tcpdump net-tools iproute2 iputils-ping && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -f requirements.txt

