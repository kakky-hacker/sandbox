from random import randint
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()

g_time = Gauge('job_last_complete_unixtime', 'Last time a batch job completed', registry=registry)
g_time.set_to_current_time()

g_num = Gauge('job_random_number', 'random number', registry=registry)
g_num.set(randint(1, 20))

push_to_gateway('localhost:9091', job='my-job', registry=registry)
