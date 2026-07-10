import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# 🔧 SMTP Settings (Recommend using Environment Variables later)
# For testing, you can change these values directly
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "jo.xaysongkham99@gmail.com"  # 👈 Your email
SMTP_PASSWORD = "aqcq nuby tdii ziup"    # 👈 App Password from Google


def send_reset_password_email(target_email: str, token: str):
    # Correct link for your project
    reset_link = f"http://localhost:5173/Savannakhet-Project/#/reset-password?token={token}"

    # Create email content
    message = MIMEMultipart("alternative")
    message["Subject"] = "Savannakhet Smart Travel - Reset Your Password"
    message["From"] = f"Savannakhet Support <{SMTP_USERNAME}>"
    message["To"] = target_email

    # Plain text
    text = f"Hello,\n\nPlease use the following link to reset your password:\n{reset_link}\n\nIf you did not request this, please ignore this email."

    # HTML (for better looks)
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
            <h2 style="color: #00aa6c;">Savannakhet Smart Travel</h2>
            <p>Hello,</p>
            <p>You requested to reset your password. Please click the button below to set a new password:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" 
                   style="background-color: #0f172a; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                   Reset Password
                </a>
            </div>
            <p>Or copy and paste this link into your browser:</p>
            <p><a href="{reset_link}">{reset_link}</a></p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 0.8rem; color: #777;">If you did not request this, please ignore this email.</p>
        </div>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    try:
        # Connect and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Encrypt data
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, target_email, message.as_string())
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False
