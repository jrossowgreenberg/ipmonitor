FROM python:3.13-slim-bookworm

WORKDIR /app

COPY ipmonitor.py .

RUN pip install requests apprise

ENV VERSION=0.1.3
ENV CHECK_INTERVAL=60
ENV APPRISE_URLS=[]
ENV MAX_FAILURES=3

CMD ["python", "ipmonitor.py"]