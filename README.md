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