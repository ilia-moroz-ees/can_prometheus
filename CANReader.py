import can
import logging
from typing import Optional, Dict


class CANReader:
    def __init__(self, interface: str = 'virtual', channel: str = 'vcan0'):
        """
        Initialize CAN reader for virtual CAN interface

        Args:
            interface: Type of interface ('virtual', 'socketcan', etc.)
            channel: CAN interface name (e.g., 'vcan0')
        """
        self.interface = interface
        self.channel = channel
        self.bus = None
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Configure logging for CAN messages"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('CANReader')

    def connect(self) -> bool:
        """Establish connection to CAN bus"""
        try:
            self.bus = can.interface.Bus(
                interface=self.interface,
                channel=self.channel,
                receive_own_messages=False
            )
            self.logger.info(f"Connected to {self.channel}")
            return True
        except Exception as e:
            self.logger.error(f"Connection failed: {str(e)}")
            return False

    def read_message(self, timeout: float = 1.0) -> Optional[can.Message]:
        """
        Read a single CAN message

        Args:
            timeout: Seconds to wait for message
        Returns:
            can.Message or None if timeout/no message
        """
        try:
            msg = self.bus.recv(timeout=timeout)
            if msg is not None:
                self._log_message(msg)
            return msg
        except can.CanError as e:
            self.logger.error(f"Read error: {str(e)}")
            return None

    def _log_message(self, msg: can.Message):
        """Log CAN message in human-readable format"""
        data_str = ' '.join(f"{byte:02X}" for byte in msg.data)
        self.logger.info(
            f"ID: {msg.arbitration_id:04X} | "
            f"Data: {data_str} | "
            f"Timestamp: {msg.timestamp:.6f}"
        )

    def shutdown(self):
        """Cleanup CAN connection"""
        if self.bus:
            self.bus.shutdown()
            self.logger.info("CAN connection closed")


if __name__ == "__main__":
    # Example usage
    reader = CANReader(interface = 'socketcan', channel='vcan0')

    if reader.connect():
        try:
            while True:
                msg = reader.read_message()
                # Just print messages for now
                # We'll process them later
        except KeyboardInterrupt:
            reader.shutdown()
