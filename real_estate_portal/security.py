"""
Security utility functions for DreamHome Real Estate Portal.
Provides functions for password validation, token generation, and other security operations.
"""
import re
from datetime import datetime, timedelta
import secrets
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

def validate_password(password):
    """
    Validate password against security policy.
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if len(password) < current_app.config['PASSWORD_MIN_LENGTH']:
        return False, f"Password must be at least {current_app.config['PASSWORD_MIN_LENGTH']} characters long"
        
    if current_app.config['PASSWORD_REQUIRE_UPPERCASE']:
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
            
    if current_app.config['PASSWORD_REQUIRE_LOWERCASE']:
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
            
    if current_app.config['PASSWORD_REQUIRE_NUMBERS']:
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
            
    if current_app.config['PASSWORD_REQUIRE_SPECIAL']:
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
            
    return True, "Password is valid"

def generate_reset_token(user_email):
    """
    Generate a secure password reset token.
    
    Args:
        user_email (str): Email of the user requesting password reset
        
    Returns:
        str: Reset token
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    """
    Verify a password reset token.
    
    Args:
        token (str): The token to verify
        expiration (int): Token expiration time in seconds (default: 1 hour)
        
    Returns:
        str or None: User email if valid, None if invalid
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )
        return email
    except:
        return None

def generate_secure_password():
    """
    Generate a secure random password that meets all requirements.
    
    Returns:
        str: Secure password
    """
    # Define character sets
    upper = 'ABCDEFGHJKLMNPQRSTUVWXYZ'  # Excluding I and O
    lower = 'abcdefghijkmnpqrstuvwxyz'  # Excluding l and o
    digits = '23456789'  # Excluding 0 and 1
    special = '!@#$%^&*'
    
    # Generate one character from each required set
    pwd = [
        secrets.choice(upper),
        secrets.choice(lower),
        secrets.choice(digits),
        secrets.choice(special)
    ]
    
    # Add additional random characters to meet minimum length
    all_chars = upper + lower + digits + special
    while len(pwd) < current_app.config['PASSWORD_MIN_LENGTH']:
        pwd.append(secrets.choice(all_chars))
    
    # Shuffle the password
    pwd = list(pwd)
    secrets.SystemRandom().shuffle(pwd)
    return ''.join(pwd)

def hash_password(password):
    """
    Hash a password using the configured method.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=32)
