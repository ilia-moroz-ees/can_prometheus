from prometheus_client import start_http_server, Counter, Gauge
from config import *
import logging
import random
import time

# Create metrics
# REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP requests')
# TEMPERATURE_GAUGE = Gauge('temperature_celsius', 'Current temperature')

# if __name__ == '__main__':
#     # Start HTTP server on port 8000
#     start_http_server(8000)
#     print("Prometheus metrics available at http://localhost:8000/metrics")
    
#     # Simulate some metrics changing
#     while True:
#         # Increment the counter
#         REQUEST_COUNTER.inc()
        
#         # Set the temperature to a random value
#         TEMPERATURE_GAUGE.set(random.uniform(18.0, 25.0))
        
#         # Wait for 2 seconds
#         time.sleep(2)

class PrometheusClient:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.gauges = {} # dictionary of format: {gauge_name : Gauge()}

        try:
            start_http_server(SERVER_PORT)
            self.logger.info("Prometheus metrics available at http://localhost:8000/metrics")
        
        except Exception as e:
            self.logger.error(f"Failed to start the server: {str(e)}")
            raise

    def send_message(self, message):
        if message:
            signals = message["signals"]

            if message["message_name"] not in self.gauges.keys(): # Add Gauge if not added yet
                gauge = Gauge(
                    message["message_name"],
                    "",
                    ["signal"]
                )
                self.gauges[gauge._get_metric().name] = gauge 
            for sig in signals.keys():
                self.gauges[message["message_name"]].labels(signal = sig).set(signals[sig])


if __name__ == "__main__":
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT
    )

    client = PrometheusClient()
    message = {
        'timestamp': 0,
        'message_name': "AIN_Volt_FB",
        'signals': {"AIN_E4" : 10, "AIN_D4" : 20}
    }
    client.send_message(message)
    while True:
        pass