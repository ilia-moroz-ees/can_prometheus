from pathlib import Path

# CAN Interface Configuration
CAN_INTERFACE = 'socketcan'  # or 'virtual', 'kvaser', etc.
CAN_CHANNEL = 'vcan0'        # or 'can0', 'can1', etc.

# DBC Configuration
DBC_FILE_PATHS = [
    "ttc_io_30xh_d65.dbc"
]

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

SERVER_PORT = 8000