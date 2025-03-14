import aiohttp
import aiosmtplib
from twilio.rest import Client
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AlertCoordinator:
    def __init__(self, db):
        self.db = db
        self.twilio = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN')) \
            if os.getenv('TWILIO_SID') else None
        self.alert_timestamps = []

    async def trigger_alert(self, title, details, severity):
        now = datetime.now()
        self.alert_timestamps = [ts for ts in self.alert_timestamps if now - ts < timedelta(minutes=1)]
        if len(self.alert_timestamps) < 100:  # Limit 100 alertów na minutę
            self.alert_timestamps.append(now)
            await self.db.log_alert(severity, None, f"{title}: {details}")
            await self._send_slack(title, details, severity)
            await self._send_email(title, details, severity)
            self._send_sms(title, details)
        else:
            logger.warning(f"Alert rate limit exceeded: {title}")

    async def _send_slack(self, title, details, severity):
        webhook = os.getenv('SLACK_WEBHOOK')
        if not webhook:
            return
        
        async with aiohttp.ClientSession() as session:
            await session.post(webhook, json={
                "text": f"*{title}* ({severity})\n{details}"
            })

    async def _send_email(self, title, details, severity):
        if not all(os.getenv(k) for k in ['SMTP_USER', 'SMTP_PASS']):
            return
        
        message = f"Subject: [CyberWitness] {title}\n\n{details}"
        async with aiosmtplib.SMTP(
            hostname=os.getenv('SMTP_HOST', 'smtp.gmail.com'),
            port=465,
            use_tls=True
        ) as smtp:
            await smtp.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
            await smtp.sendmail(
                os.getenv('SMTP_USER'),
                os.getenv('ALERT_EMAILS').split(','),
                message
            )

    def _send_sms(self, title, details):
        if not self.twilio:
            return
        
        self.twilio.messages.create(
            body=f"[CyberWitness] {title}: {details[:160]}",
            from_=os.getenv('TWILIO_NUMBER'),
            to=os.getenv('ADMIN_PHONE')
        )