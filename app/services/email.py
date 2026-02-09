import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

def send_password_reset_email(to_email: str, reset_token: str):
    """
    Send password reset email to user
    
    Args:
        to_email: Recipient's email address
        reset_token: Token for password reset
    """
    # Create reset link
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    
    # Email content
    subject = "Set Your Password - Lead Management System"
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #4CAF50;">Welcome to Lead Management System!</h2>
                
                <p>You have been invited to join our Lead Management System.</p>
                
                <p>To set your password and complete your profile, please click the button below:</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" 
                       style="background-color: #4CAF50; 
                              color: white; 
                              padding: 12px 30px; 
                              text-decoration: none; 
                              border-radius: 5px;
                              display: inline-block;">
                        Set Your Password
                    </a>
                </div>
                
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{reset_link}</p>
                
                <p style="color: #999; font-size: 12px; margin-top: 30px;">
                    This link will expire in 24 hours. If you didn't request this, please ignore this email.
                </p>
            </div>
        </body>
    </html>
    """
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>"
    message["To"] = to_email
    
    # Attach HTML content
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)
    
    # Send email
    try:
        print(f"📧 Attempting to send email to {to_email}...")
        print(f"   SMTP Host: {settings.SMTP_HOST}")
        print(f"   SMTP Port: {settings.SMTP_PORT}")
        print(f"   SMTP User: {settings.SMTP_USER}")
        print(f"   From Email: {settings.FROM_EMAIL}")
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            server.set_debuglevel(0)  # Set to 1 for detailed SMTP logs
            print("   ✓ Connected to SMTP server")
            
            server.starttls()
            print("   ✓ TLS started")
            
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            print("   ✓ Login successful")
            
            server.send_message(message)
            print(f"   ✓ Message sent successfully")
            
        print(f"✅ Password reset email sent to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {str(e)}")
        print("   → Check your SMTP_USER and SMTP_PASSWORD in .env")
        print("   → Make sure you're using Gmail App Password, not regular password")
        print("   → Enable 2FA at: https://myaccount.google.com/signinoptions/two-step-verification")
        print("   → Get App Password at: https://myaccount.google.com/apppasswords")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {str(e)}")
        return False
        
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        return False