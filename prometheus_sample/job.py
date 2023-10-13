import time
from random import randint
import logging

logging.basicConfig(level=logging.INFO)

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


def main():
    registry = CollectorRegistry()
    g_time = Gauge('job_last_complete_unixtime', 'Last time a batch job completed', registry=registry)
    g_num = Gauge('job_random_number', 'random number', ['id'], registry=registry)

    while True:
        g_time.set_to_current_time()
        g_num.labels(id='aaa').set(randint(1, 20))
        g_num.labels(id='bbb').set(randint(1, 20))

        push_to_gateway('localhost:9091', job='my-job', registry=registry)

        logging.info("push metrics!!")

        time.sleep(3)

if __name__ == "__main__":
    main()
