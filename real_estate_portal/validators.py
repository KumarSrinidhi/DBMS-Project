"""
Custom validator functions for DreamHome Real Estate Portal forms.
Extends the WTForms validators with additional validation logic.
"""
import re
from wtforms.validators import ValidationError


def validate_phone_number(form, field):
    """
    Validate that the field contains a valid Indian phone number format.
    
    Args:
        form: The form containing the field
        field: The field to validate
    
    Raises:
        ValidationError: If the phone number is invalid
    """
    if not field.data:
        return
        
    # Remove any whitespace
    phone = field.data.strip()
    
    # Check if it's a valid Indian phone number (10 digits, optionally prefixed with +91)
    if re.match(r'^(\+91)?[6-9]\d{9}$', phone) is None:
        raise ValidationError('Invalid Indian phone number format. Please enter a 10-digit number.')


def validate_pan_number(form, field):
    """
    Validate that the field contains a valid Indian PAN card number.
    
    Args:
        form: The form containing the field
        field: The field to validate
    
    Raises:
        ValidationError: If the PAN number is invalid
    """
    if not field.data:
        return
        
    # PAN format: 5 letters, 4 numbers, 1 letter
    pan = field.data.strip().upper()
    
    if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan) is None:
        raise ValidationError('Invalid PAN number format. Please enter a valid PAN.')


def validate_pincode(form, field):
    """
    Validate that the field contains a valid Indian PIN code.
    
    Args:
        form: The form containing the field
        field: The field to validate
    
    Raises:
        ValidationError: If the PIN code is invalid
    """
    if not field.data:
        return
        
    # PIN code format: 6 digits
    pin = field.data.strip()
    
    if re.match(r'^[1-9][0-9]{5}$', pin) is None:
        raise ValidationError('Invalid PIN code. Please enter a valid 6-digit PIN code.')