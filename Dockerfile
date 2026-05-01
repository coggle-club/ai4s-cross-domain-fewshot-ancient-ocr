FROM python:3.11-slim

ENV TZ=Asia/Shanghai \
    LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /app /saisresult && \
    apt-get update && \
    apt-get install -y tini bash \
        libxcb-xinerama0 \
        libxcb-shape0 \
        libxcb-xfixes0 \
        libxcb-randr0 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-icccm4 \
        libxcb-shm0 \
        libxcb-util1 \
        libxcb-render-util0 \
        libxcb-render0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libfontconfig1 \
        libcairo2 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENTRYPOINT ["/sbin/tini", "--", "bash", "/app/run.sh"]