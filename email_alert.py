import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import EDR_CONFIG

class EmailAlert:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.smtp_config = EDR_CONFIG.get('smtp', {})
    
    def send_alert(self, alert_data):
        if not EDR_CONFIG.get('email_alerts'):
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_config['username']
            msg['To'] = self.smtp_config['to_email']
            msg['Subject'] = f"EDR Alert: {alert_data.get('type', 'Unknown')}"
            
            body = f"""
            EDR Security Alert
            
            Type: {alert_data.get('type')}
            Risk Level: {alert_data.get('risk_level')}
            Time: {alert_data.get('timestamp')}
            
            Details: {alert_data}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['username'], self.smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info("Alert email sent successfully")
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
