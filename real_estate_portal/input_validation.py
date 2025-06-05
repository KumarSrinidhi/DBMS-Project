"""
Input validation and sanitization utilities for DreamHome Real Estate Portal.
"""
import re
import bleach
from flask import current_app
from PIL import Image
import magic
import os

def sanitize_html(html_content):
    """
    Sanitize HTML content to prevent XSS attacks.
    
    Args:
        html_content (str): Raw HTML content
        
    Returns:
        str: Sanitized HTML content
    """
    allowed_tags = [
        'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'ul', 'ol', 'li', 'span', 'div', 'b', 'i'
    ]
    
    allowed_attrs = {
        '*': ['class', 'style'],
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'title', 'width', 'height']
    }
    
    allowed_styles = [
        'color', 'font-weight', 'text-align', 'font-size',
        'font-family', 'line-height', 'letter-spacing',
        'text-decoration', 'font-style'
    ]
    
    return bleach.clean(
        html_content,
        tags=allowed_tags,
        attributes=allowed_attrs,
        styles=allowed_styles,
        strip=True
    )

def validate_image_file(file_storage):
    """
    Validate uploaded image file for security and quality.
    
    Args:
        file_storage: FileStorage object from Flask
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    # Check file size
    if len(file_storage.read()) > current_app.config['MAX_CONTENT_LENGTH']:
        return False, "File size exceeds maximum limit"
    file_storage.seek(0)  # Reset file pointer
    
    # Check MIME type
    mime = magic.from_buffer(file_storage.read(), mime=True)
    file_storage.seek(0)
    
    if mime not in ['image/jpeg', 'image/png', 'image/gif']:
        return False, "Invalid file type. Only JPEG, PNG and GIF are allowed"
    
    try:
        with Image.open(file_storage) as img:
            # Check image dimensions
            if any(dim > 4096 for dim in img.size):
                return False, "Image dimensions too large"
            
            # Verify it's a valid image file
            img.verify()
            
            return True, "Image is valid"
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"

def validate_indian_phone(phone):
    """
    Validate Indian phone number format.
    
    Args:
        phone (str): Phone number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^(\+91[\-\s]?)?[6789]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_pan(pan):
    """
    Validate Indian PAN card number.
    
    Args:
        pan (str): PAN number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    return bool(re.match(pattern, pan))

def validate_aadhaar(aadhaar):
    """
    Validate Aadhaar number using Verhoeff algorithm.
    
    Args:
        aadhaar (str): Aadhaar number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Remove spaces and check length
    aadhaar = aadhaar.replace(" ", "")
    if not re.match(r'^\d{12}$', aadhaar):
        return False
    
    # Verhoeff algorithm implementation
    mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
    
    perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]
    
    def checksum(number):
        c = 0
        for i, item in enumerate(reversed(str(number))):
            c = mult[c][perm[i % 8][int(item)]]
        return c
    
    return checksum(aadhaar) == 0

def validate_email(email):
    """
    Validate email address format and domain.
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False
        
    # Additional checks could be added here:
    # - Domain MX record check
    # - Disposable email domain check
    # - Company domain whitelist/blacklist
    
    return True

def sanitize_filename(filename):
    """
    Sanitize a filename to prevent path traversal attacks.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Remove path separators and null bytes
    filename = os.path.basename(filename)
    filename = filename.replace('\x00', '')
    
    # Remove potentially dangerous characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    
    # Ensure it doesn't start with a dot (hidden file)
    filename = filename.lstrip('.')
    
    return filename if filename else 'unnamed_file'
