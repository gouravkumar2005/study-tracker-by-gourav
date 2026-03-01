import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime

class NotificationSystem:
    def __init__(self):
        self.email_enabled = False
        self.whatsapp_enabled = False
        
    def send_email(self, to_email, subject, message):
        """Send email notification"""
        try:
            # Using Gmail SMTP (user needs to configure)
            from_email = "studytracker@gmail.com"  # Configure this
            password = "your_app_password"  # Configure this
            
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Email error: {e}")
            return False
    
    def send_whatsapp(self, phone_number, message):
        """Send WhatsApp notification using Twilio"""
        try:
            # Using Twilio API (user needs to configure)
            account_sid = "your_account_sid"
            auth_token = "your_auth_token"
            from_whatsapp = "whatsapp:+14155238886"
            to_whatsapp = f"whatsapp:{phone_number}"
            
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            
            data = {
                'From': from_whatsapp,
                'To': to_whatsapp,
                'Body': message
            }
            
            response = requests.post(url, data=data, auth=(account_sid, auth_token))
            return response.status_code == 201
        except Exception as e:
            print(f"WhatsApp error: {e}")
            return False
    
    def notify_session_start(self, student_name, parent_contact):
        """Notify parent when session starts"""
        message = f"📚 {student_name} started a study session at {datetime.now().strftime('%I:%M %p')}"
        self._send_notification(parent_contact, "Study Session Started", message)
    
    def notify_session_end(self, student_name, parent_contact, hours, focus_score):
        """Notify parent when session ends"""
        message = f"✅ {student_name} completed {hours}h study session\nFocus Score: {focus_score}%"
        self._send_notification(parent_contact, "Study Session Completed", message)
    
    def notify_low_focus(self, student_name, parent_contact, focus_score):
        """Alert parent about low focus"""
        message = f"⚠️ {student_name}'s focus dropped to {focus_score}%\nDistraction detected!"
        self._send_notification(parent_contact, "Low Focus Alert", message)
    
    def notify_distraction(self, student_name, parent_contact, activity):
        """Alert parent about specific distraction"""
        message = f"🚨 {student_name} is distracted!\nActivity: {activity}"
        self._send_notification(parent_contact, "Distraction Alert", message)
    
    def _send_notification(self, contact, subject, message):
        """Send notification via available channels"""
        if '@' in contact:
            self.send_email(contact, subject, message)
        elif contact.startswith('+'):
            self.send_whatsapp(contact, message)
