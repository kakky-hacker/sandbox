## Build image for python server
```
docker buildx build . --tag sample-server --platform=linux/amd64
```

## Run servers
```
docker-compose up -d
```

## Add request count (metric : http_get_requests_total)
```
curl http://localhost:8080
```

## Add exception count (metric : exceptions_total)
```
curl http://localhost:8080/error
```

## Push last time a batch job completed (metric : job_last_complete_unixtime)
```
python job.py
```
