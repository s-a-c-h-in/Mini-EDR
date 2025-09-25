EDR_CONFIG = {
    'email_alerts': False,  # Set to True to enable
    'log_level': 'INFO',
    'monitoring_interval': 2,
    
    'smtp': {
        'server': 'smtp.gmail.com',
        'port': 587,
        'username': 'your-email@gmail.com',
        'password': 'your-app-password',
        'to_email': 'alerts@company.com'
    },
    
    'file_monitoring': {
        'paths': {
            'windows': ['C:\\Users', 'C:\\Windows\\Temp'],
            'linux': ['/home', '/tmp', '/etc'],
            'darwin': ['/Users', '/tmp']
        },
        'ignore_extensions': ['.log', '.tmp', '.cache']
    },
    
    'blocked_ips': [],
    'whitelist_processes': ['chrome.exe', 'firefox.exe', 'notepad.exe']
}
