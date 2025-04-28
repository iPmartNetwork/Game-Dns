FROM coredns/coredns:latest

RUN apk add --no-cache python3 py3-pip sqlite

COPY app /app
COPY Corefile /Corefile

WORKDIR /app
RUN pip3 install flask

EXPOSE 53/udp
EXPOSE 53/tcp
EXPOSE 5000

CMD ["sh", "-c", "python3 app.py & coredns -conf /Corefile"]