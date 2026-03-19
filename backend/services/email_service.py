import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "mail.groovedonkey.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER", "patino@groovedonkey.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "patino@groovedonkey.com")


def send_contact_notification(
    first_name: str, last_name: str, business_name: str,
    phone: str, email: str, interest: str, message: str,
):
    """Send an email notification when a new contact form is submitted."""
    if not all([SMTP_USER, SMTP_PASSWORD, NOTIFY_EMAIL]):
        logger.warning("Email not configured — skipping notification.")
        return

    full_name = f"{first_name} {last_name}"
    subject = f"New Contact Form Submission from {full_name}"

    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #D4AF37;">New Contact Form Submission</h2>
        <table style="border-collapse: collapse; width: 100%; max-width: 500px;">
            <tr>
                <td style="padding: 8px; font-weight: bold; border-bottom: 1px solid #eee;">Name</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{full_name}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; border-bottom: 1px solid #eee;">Business</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{business_name or "Not provided"}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; border-bottom: 1px solid #eee;">Phone</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{phone}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; border-bottom: 1px solid #eee;">Email</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;"><a href="mailto:{email}">{email}</a></td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; border-bottom: 1px solid #eee;">Interested In</td>
                <td style="padding: 8px; border-bottom: 1px solid #eee;">{interest}</td>
            </tr>
            <tr>
                <td style="padding: 8px; font-weight: bold; vertical-align: top;">Comments</td>
                <td style="padding: 8px;">{message or "None"}</td>
            </tr>
        </table>
        <p style="margin-top: 20px; color: #888; font-size: 12px;">
            This notification was sent from jasonpatino.com contact form.
        </p>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = NOTIFY_EMAIL
    msg["Reply-To"] = email
    msg.attach(MIMEText(html_body, "html"))

    try:
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_USER, NOTIFY_EMAIL, msg.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.sendmail(SMTP_USER, NOTIFY_EMAIL, msg.as_string())
        logger.info(f"Notification email sent for contact '{full_name}'.")
    except Exception as e:
        logger.error(f"Failed to send notification email: {e}")
