FROM python:3.11-slim

ENV TZ=Asia/Shanghai \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /app /saisresult && \
    apt-get update && \
    apt-get install -y tini bash && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/src/
RUN chmod +x /app/src/run.sh

ENTRYPOINT ["/sbin/tini", "--", "bash", "/app/src/run.sh"]