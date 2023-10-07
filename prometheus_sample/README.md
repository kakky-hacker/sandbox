## Build image for python server
```
docker buildx build . --tag sample-server --platform=linux/amd64
```

## Run servers
```
docker-compose up -d
```

## Get
```
curl http://localhost:8080
```

## Metrics
```
curl http://localhost:8000/metrics
```
