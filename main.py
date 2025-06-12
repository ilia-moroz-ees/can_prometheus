import logging
from config import *
from CANReader import CANReader
from DBCDecoder import DBCDecoder
from prometheusClient import PrometheusClient

def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT
    )

def main():
    setup_logging()
    logger = logging.getLogger('main')
    client = PrometheusClient()

    # Initialize DBC decoder
    dbc_decoder = None
    if DBC_FILE_PATHS:
        logger.info("Initializing DBC decoder...")
        dbc_decoder = DBCDecoder(DBC_FILE_PATHS)

    # Initialize CAN reader
    logger.info("Initializing CAN reader...")
    can_reader = CANReader(
        interface=CAN_INTERFACE,
        channel=CAN_CHANNEL,
        dbc_decoder=dbc_decoder
    )

    if not can_reader.connect():
        logger.error("Failed to initialize CAN interface")
        return

    logger.info("Starting CAN monitoring...")
    while True:
        try:
            message = can_reader.read_decoded_message()
            client.send_message(message)

        except KeyboardInterrupt: # Shutting down properly
            break


    logger.info("Shutting down...")
    can_reader.shutdown()

if __name__ == "__main__":
    main()