import os
import sys
import time
import logging
import threading
from datetime import datetime

class MiniEDR:
    def __init__(self):
        self.running = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def start(self):
        self.logger.info("Mini EDR started")
        self.running = True
        
        # Start monitors in threads
        from agents.file_monitor import FileMonitor
        from agents.process_monitor import ProcessMonitor
        from agents.network_monitor import NetworkMonitor
        
        monitors = [
            FileMonitor(self.event_callback),
            ProcessMonitor(self.event_callback),
            NetworkMonitor(self.event_callback)
        ]
        
        for monitor in monitors:
            thread = threading.Thread(target=monitor.start, daemon=True)
            thread.start()
        
        while self.running:
            time.sleep(1)
    
    def event_callback(self, event):
        self.logger.warning(f"ALERT: {event.get('type', 'unknown')}")
        if event.get('risk_level') == 'high':
            self.logger.critical(f"HIGH RISK: {event}")

if __name__ == "__main__":
    edr = MiniEDR()
    try:
        edr.start()
    except KeyboardInterrupt:
        print("EDR stopped")
