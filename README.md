# ipmonitor

## Running Docker Container 
```
docker run -d \
  --name ipmonitor \
  -e CHECK_INTERVAL=60 \
  -e APPRISE_URLS='["tgram://123456:abcdef/12345"]' \
  -e MAX_FAILURES=3 \
  -v $(pwd)/logs:/var/log \
  ipmonitor
```

# Docker Compose 
```
services:
  ipmonitor:
    image: ghcr.io/jrossowgreenberg/ipmonitor:latest
    container_name: ipmonitor
    restart: unless-stopped
    environment:
      - CHECK_INTERVAL=60
      - APPRISE_URLS=["tgram://123456:abcdef/12345"]
      - MAX_FAILURES=3
    volumes:
      - ./logs:/var/log/ipmonitor
```