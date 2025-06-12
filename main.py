from prometheus_client import start_http_server, Counter, Gauge
from asammdf import MDF
import random
import time

PORT = 8000

# Create metrics
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests')
TEMPERATURE_GAUGE = Gauge('temperature_celsius', 'Current temperature')

if __name__ == '__main__':
    # Start HTTP server on port 8000
    start_http_server(PORT)
    print(f"Prometheus metrics available at http://localhost:{PORT}/metrics")

    # Simulate some metrics changing
    while True:
        # Increment the counter
        REQUEST_COUNTER.inc()

        # Set the temperature to a random value
        TEMPERATURE_GAUGE.set(random.uniform(18.0, 25.0))

        # Wait for 2 seconds
        time.sleep(2)
