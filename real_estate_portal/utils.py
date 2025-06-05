"""
Utility functions for the DreamHome Real Estate Portal.
Contains helper functions used throughout the application.

This file contains utility functions used throughout the application.
Key responsibilities:
- Providing helper functions for file uploads, formatting, etc.
- Centralizing reusable logic to avoid code duplication
- Used by routes, models, and other modules as needed
"""

import os
import re
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename, allowed_extensions=None):
    """
    Check if a file has an allowed extension.
    
    Args:
        filename (str): The filename to check
        allowed_extensions (set): Set of allowed file extensions
        
    Returns:
        bool: True if file is allowed, False otherwise
    """
    if allowed_extensions is None:
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_unique_filename(filename):
    """
    Generate a unique filename to prevent naming conflicts.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Unique filename with UUID
    """
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
    return unique_filename


def format_currency(amount, currency='₹'):
    """
    Format a number as currency.
    
    Args:
        amount (float): The amount to format
        currency (str): Currency symbol
        
    Returns:
        str: Formatted currency string
    """
    if not amount:
        return f"{currency}0"
    
    # Format with commas for Indian numbering system (lakhs, crores)
    # 1,00,000 instead of 100,000
    amount_str = str(int(amount))
    result = ""
    
    if len(amount_str) > 3:
        result = "," + amount_str[-3:]
        amount_str = amount_str[:-3]
        
        # Process remaining groups of 2
        while len(amount_str) > 2:
            result = "," + amount_str[-2:] + result
            amount_str = amount_str[:-2]
            
        if amount_str:
            result = amount_str + result
            
        return f"{currency}{result}"
    else:
        return f"{currency}{amount_str}"


def slugify(text):
    """
    Create a URL-friendly slug from text.
    
    Args:
        text (str): Text to convert to slug
        
    Returns:
        str: URL-friendly slug
    """
    # Replace spaces with hyphens and remove special characters
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-_')
    return text