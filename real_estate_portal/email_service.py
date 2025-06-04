"""
Email handling service for DreamHome Real Estate Portal.
Provides functions for sending various types of emails to users.
"""
import os
from flask import current_app, render_template
from smtplib import SMTP, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(recipient, subject, html_content, text_content=None):
    """
    Send an email with both HTML and plain text content.
    
    Args:
        recipient (str): Recipient email address
        subject (str): Email subject
        html_content (str): HTML content of the email
        text_content (str): Plain text content (optional)
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    # Get configuration from app
    sender = current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@dreamhome.com')
    smtp_server = current_app.config.get('MAIL_SERVER', 'localhost')
    smtp_port = current_app.config.get('MAIL_PORT', 25)
    smtp_user = current_app.config.get('MAIL_USERNAME')
    smtp_pass = current_app.config.get('MAIL_PASSWORD')
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    
    # Attach text content
    if text_content:
        msg.attach(MIMEText(text_content, 'plain'))
    
    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        # Connect to SMTP server
        server = SMTP(smtp_server, smtp_port)
        
        # Use TLS if configured
        if current_app.config.get('MAIL_USE_TLS', False):
            server.starttls()
        
        # Login if credentials provided
        if smtp_user and smtp_pass:
            server.login(smtp_user, smtp_pass)
        
        # Send email
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        
        current_app.logger.info(f"Email sent to {recipient}: {subject}")
        return True
    
    except SMTPException as e:
        current_app.logger.error(f"Failed to send email to {recipient}: {str(e)}")
        return False
    except Exception as e:
        current_app.logger.error(f"Unexpected error sending email: {str(e)}")
        return False


def send_welcome_email(user):
    """
    Send a welcome email to a new user.
    
    Args:
        user: User model instance
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    subject = "Welcome to DreamHome Real Estate Portal"
    
    # Render email templates
    html_content = render_template('email/welcome.html', user=user)
    text_content = render_template('email/welcome.txt', user=user)
    
    return send_email(user.email, subject, html_content, text_content)


def send_password_reset(user, reset_token):
    """
    Send a password reset email to a user.
    
    Args:
        user: User model instance
        reset_token: Password reset token
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    subject = "Reset Your DreamHome Password"
    
    # Construct reset URL
    reset_url = f"{current_app.config.get('BASE_URL', '')}/auth/reset/{reset_token}"
    
    # Render email templates
    html_content = render_template('email/password_reset.html', 
                                  user=user, reset_url=reset_url)
    text_content = render_template('email/password_reset.txt',
                                  user=user, reset_url=reset_url)
    
    return send_email(user.email, subject, html_content, text_content)