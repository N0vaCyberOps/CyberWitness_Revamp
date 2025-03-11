import smtplib
import asyncio
import requests
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config_manager import ConfigManager

class AlertCoordinator:
    def __init__(self):
        self.config = ConfigManager()

    async def send_email_alert(self, subject, body):
        """Wysyła e-mail z alertem."""
        if not self.config.get_config("email_alerts", False):
            return
        try:
            msg = MIMEMultipart()
            msg["From"] = self.config.get_config("smtp_user")
            msg["To"] = self.config.get_config("recipient_email", "recipient@example.com")
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.config.get_config("smtp_server"), self.config.get_config("smtp_port")) as server:
                server.starttls()
                server.login(self.config.get_config("smtp_user"), self.config.get_config("smtp_password"))
                server.sendmail(msg["From"], msg["To"], msg.as_string())

            logging.info(f"Email alert sent: {subject}")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

    async def send_webhook_alert(self, message):
        """Wysyła powiadomienie do webhooka."""
        webhook_url = self.config.get_config("webhook_url")
        if not webhook_url:
            return

        try:
            response = requests.post(webhook_url, json={"alert": message})
            logging.info(f"Webhook alert sent, response: {response.status_code}")
        except Exception as e:
            logging.error(f"Error sending webhook alert: {e}")

    async def trigger_alert(self, message):
        """Wyzwala alert (e-mail + webhook)."""
        await asyncio.gather(
            self.send_email_alert("CyberWitness Alert", message),
            self.send_webhook_alert(message)
        )
