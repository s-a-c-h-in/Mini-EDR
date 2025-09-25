# Mini EDR - Quick Setup Guide

## Project Structure
```
mini-edr/
├── main.py                 # Main EDR service
├── install.py              # Installation script
├── requirements.txt        # Python dependencies
├── config/
│   ├── settings.py         # Configuration
│   └── rules.json          # Detection rules
├── agents/
│   ├── file_monitor.py     # File monitoring
│   ├── process_monitor.py  # Process monitoring  
│   └── network_monitor.py  # Network monitoring
├── database/
│   └── manager.py          # Database operations
├── alerts/
│   └── email_alert.py      # Email notifications
├── dashboard/
│   └── app.py              # Web dashboard
├── logs/                   # Log files
└── quarantine/             # Quarantined files
```

## Quick Start

### 1. Installation
```bash
# Create project directory
mkdir mini-edr && cd mini-edr

# Copy all the scripts from the artifact above into respective files

# Install dependencies
pip install psutil watchdog flask

# Or run the installer
python install.py
```

### 2. Configuration
Edit `config/settings.py` to customize:
- Email alerts (optional)
- Monitoring paths
- Detection sensitivity

### 3. Start EDR Service
```bash
# Terminal 1: Start main EDR service
python main.py

# Terminal 2: Start web dashboard  
cd dashboard && python app.py
```

### 4. Access Dashboard
Open browser: `http://localhost:5000`

## 🔧 Testing the EDR

### Test File Monitor
```bash
# Create suspicious file in temp directory
echo "test malware" > /tmp/malware.exe  # Linux
echo "test malware" > C:\Windows\Temp\malware.exe  # Windows
```

### Test Process Monitor
```bash
# Start suspicious process
nc -l 4444                    # Linux/Mac
powershell -enc "test"        # Windows
```

### Test Network Monitor  
```bash
# Make connection to suspicious IP (configure in settings)
ping 192.168.100.100
curl http://192.168.100.100:4444
```

## Dashboard Features

- **Real-time Monitoring**: Live event feed
- **System Health**: CPU, memory, process count
- **Security Alerts**: Risk-based notifications  
- **Event History**: Recent security events
- **Threat Statistics**: Detection metrics

## Important Notes

1. **Run as Administrator/Root**: Required for full monitoring capabilities
2. **Educational Purpose**: This is a learning tool, not production-ready
3. **Resource Usage**: Monitors consume CPU/memory - adjust intervals as needed
4. **False Positives**: Fine-tune detection rules to reduce noise

## What It Monitors

### File System
- ✅ Executable files in temp directories
- ✅ Rapid file changes (ransomware detection)
- ✅ Large file creation
- ✅ System file modifications

### Processes  
- ✅ Suspicious process names (nc, powershell, etc.)
- ✅ Malicious command line patterns
- ✅ Unexpected parent-child relationships

### Network
- ✅ Connections to malicious IPs
- ✅ Suspicious port usage
- ✅ External network connections
- ✅ Port scanning detection

## Alert Levels

- ** Critical**: Immediate threat (malicious IP, ransomware)
- ** High**: Suspicious activity (unknown executables)  
- ** Medium**: Unusual behavior (external connections)
- ** Low**: Normal activity (logged for reference)

## Customization

### Add Custom Rules
Edit `config/rules.json`:
```json
{
  "file_rules": [
    {
      "id": "custom_rule",
      "name": "My Custom Detection", 
      "severity": "high"
    }
  ]
}
```

### Whitelist Processes
Edit `config/settings.py`:
```python
'whitelist_processes': ['chrome.exe', 'firefox.exe', 'your-app.exe']
```

### Email Alerts
Configure SMTP in `config/settings.py`:
```python
'email_alerts': True,
'smtp': {
    'server': 'smtp.gmail.com',
    'username': 'your-email@gmail.com', 
    'password': 'your-app-password'
}
```

## Troubleshooting

### EDR Won't Start
```bash
# Check Python version (3.8+ required)
python --version

# Install missing packages
pip install psutil watchdog flask

# Check permissions
sudo python main.py  # Linux/Mac
```

### Dashboard Not Loading
```bash
# Check if Flask is running
netstat -an | grep 5000

# Start dashboard manually
cd dashboard && python app.py
```

### No Alerts Showing
- Check if you're running as admin/root
- Verify monitoring paths exist
- Test with sample malware files
- Check logs in `logs/edr.log`

## Performance Tips

- Reduce monitoring frequency for better performance
- Exclude large directories from file monitoring  
- Use specific paths instead of recursive monitoring
- Adjust detection thresholds to reduce false positives

## Contributing

Ways to enhance the EDR:
- Add YARA rule integration
- Implement machine learning detection
- Create mobile alerts
- Add more threat intelligence feeds
- Improve dashboard with charts/graphs

## License

MIT License - Feel free to modify and distribute for educational purposes.

---

**⚠️ Disclaimer**: This is an educational EDR system. Do not rely on it for production security. Use commercial EDR solutions for real-world protection.

**Made with ❤️ for cybersecurity education**
