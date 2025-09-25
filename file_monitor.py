import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        self.logger = logging.getLogger(__name__)
        
    def on_created(self, event):
        if not event.is_directory:
            self.check_file(event.src_path, 'created')
    
    def on_modified(self, event):
        if not event.is_directory:
            self.check_file(event.src_path, 'modified')
    
    def check_file(self, path, action):
        risk = 'low'
        alerts = []
        
        # Check suspicious extensions
        if path.lower().endswith(('.exe', '.scr', '.bat', '.vbs')):
            if 'temp' in path.lower() or 'tmp' in path.lower():
                risk = 'high'
                alerts.append('executable_in_temp')
        
        # Check file size (potential data exfiltration)
        try:
            if os.path.getsize(path) > 100*1024*1024:  # 100MB
                risk = 'medium'
                alerts.append('large_file_created')
        except:
            pass
        
        if risk != 'low':
            self.callback({
                'type': 'file',
                'action': action,
                'path': path,
                'risk_level': risk,
                'alerts': alerts,
                'timestamp': time.time()
            })

class FileMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.observer = Observer()
        self.handler = FileEventHandler(callback)
        
    def start(self):
        # Monitor common directories
        paths = [os.path.expanduser('~'), '/tmp'] if os.name != 'nt' else [
            os.path.expanduser('~'), 'C:\\Windows\\Temp'
        ]
        
        for path in paths:
            if os.path.exists(path):
                self.observer.schedule(self.handler, path, recursive=True)
        
        self.observer.start()
        logging.info("File monitor started")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
