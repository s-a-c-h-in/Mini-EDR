import psutil
import time
import logging

class NetworkMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.known_connections = set()
        self.malicious_ips = {'192.168.100.100', '10.0.0.1'}  # Example IPs
        
    def start(self):
        logging.info("Network monitor started")
        
        while True:
            try:
                current_conns = set()
                for conn in psutil.net_connections(kind='inet'):
                    if conn.raddr:
                        conn_id = f"{conn.raddr.ip}:{conn.raddr.port}"
                        current_conns.add(conn_id)
                        
                        if conn_id not in self.known_connections:
                            self.check_connection(conn)
                
                self.known_connections = current_conns
                time.sleep(3)
                
            except Exception as e:
                logging.error(f"Network monitor error: {e}")
                time.sleep(10)
    
    def check_connection(self, conn):
        risk = 'low'
        alerts = []
        
        if conn.raddr:
            remote_ip = conn.raddr.ip
            remote_port = conn.raddr.port
            
            # Check malicious IPs
            if remote_ip in self.malicious_ips:
                risk = 'critical'
                alerts.append('malicious_ip_connection')
            
            # Check suspicious ports
            if remote_port in [4444, 4445, 5555, 6666]:
                risk = 'high'
                alerts.append('suspicious_port')
            
            # Check external connections
            if not self.is_internal_ip(remote_ip):
                risk = 'medium'
                alerts.append('external_connection')
        
        if risk != 'low':
            self.callback({
                'type': 'network',
                'remote_ip': remote_ip,
                'remote_port': remote_port,
                'pid': conn.pid,
                'risk_level': risk,
                'alerts': alerts,
                'timestamp': time.time()
            })
    
    def is_internal_ip(self, ip):
        return (ip.startswith('192.168.') or ip.startswith('10.') or 
                ip.startswith('172.') or ip == '127.0.0.1')
