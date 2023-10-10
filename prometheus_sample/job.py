from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()
g = Gauge('job_last_complete_unixtime', 'Last time a batch job completed', registry=registry)
g.set_to_current_time()
push_to_gateway('localhost:9091', job='cronJobA', registry=registry)
