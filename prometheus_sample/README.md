Build image for python server
```
docker buildx build . --tag sample-server --platform=linux/amd64
```

Run servers
```
docker-compose up -d
```

Add request count
```
curl http://localhost:8080
```

Add Exception count
```
curl http://localhost:8080/error
```

Metrics
```
curl http://localhost:8000/metrics
```