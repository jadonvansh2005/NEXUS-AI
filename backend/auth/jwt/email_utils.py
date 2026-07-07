import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.settings import settings

def send_verification_email(email: str, otp: str) -> bool:
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    sender_email = settings.SMTP_SENDER_EMAIL
    sender_password = settings.SMTP_SENDER_PASSWORD

    subject = "UPSS Email Verification Code"
    body = f"""Hello,

Thank you for registering with UPSS. Your verification code is:

{otp}

This code is valid for 10 minutes. If you did not register for an account, please ignore this email.

Best regards,
The UPSS Team"""

    # Mock mode check: If SMTP credentials are not configured, print to uvicorn console
    if not sender_email or not sender_password:
        print("\n" + "=" * 60)
        print("📧 [MOCK EMAIL SENDER] SMTP credentials not set in .env")
        print(f"To: {email}")
        print(f"Subject: {subject}")
        print(f"OTP Verification Code: {otp}")
        print("=" * 60 + "\n", flush=True)
        return True

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [email], msg.as_string())
        server.quit()
        print(f"📧 Verification email successfully sent to {email}", flush=True)
        return True
    except Exception as e:
        print(f"❌ Failed to send verification email over SMTP: {e}", flush=True)
        # Fallback to console print so developers/users can still test
        print("\n" + "=" * 60)
        print(f"📧 [FALLBACK MOCK EMAIL] SMTP Delivery Failed: {e}")
        print(f"To: {email}")
        print(f"OTP Verification Code: {otp}")
        print("=" * 60 + "\n", flush=True)
        return False
