import psutil
import time
import logging

class ProcessMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.known_pids = set()
        self.suspicious_names = {'nc', 'netcat', 'powershell', 'cmd'}
        
    def start(self):
        logging.info("Process monitor started")
        
        # Get initial processes
        for proc in psutil.process_iter(['pid']):
            self.known_pids.add(proc.info['pid'])
        
        while True:
            try:
                current_pids = set()
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    pid = proc.info['pid']
                    current_pids.add(pid)
                    
                    if pid not in self.known_pids:
                        self.check_process(proc.info)
                
                self.known_pids = current_pids
                time.sleep(2)
                
            except Exception as e:
                logging.error(f"Process monitor error: {e}")
                time.sleep(5)
    
    def check_process(self, proc_info):
        risk = 'low'
        alerts = []
        name = proc_info.get('name', '').lower()
        
        # Check suspicious process names
        if any(sus in name for sus in self.suspicious_names):
            risk = 'high'
            alerts.append('suspicious_process_name')
        
        # Check command line
        cmdline = ' '.join(proc_info.get('cmdline', [])).lower()
        if any(pattern in cmdline for pattern in ['powershell -enc', 'downloadstring', 'invoke-expression']):
            risk = 'high'
            alerts.append('suspicious_cmdline')
        
        if risk != 'low':
            self.callback({
                'type': 'process',
                'name': name,
                'pid': proc_info['pid'],
                'cmdline': cmdline,
                'risk_level': risk,
                'alerts': alerts,
                'timestamp': time.time()
            })
