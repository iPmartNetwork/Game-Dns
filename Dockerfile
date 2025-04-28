FROM python:3.11-slim

RUN apt update && apt install -y sqlite3 && pip install flask

WORKDIR /app

COPY app/ /app/
COPY backup/ /backup/
COPY Corefile /Corefile

EXPOSE 53/udp
EXPOSE 53/tcp
EXPOSE 5000

CMD ["sh", "-c", "python3 main.py & coredns -conf /Corefile"]
