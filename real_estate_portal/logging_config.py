"""
Logging configuration and utilities for DreamHome Real Estate Portal.
Sets up structured logging with different handlers for various log levels.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime
from flask import has_request_context, request, current_app
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        # Add timestamp
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().isoformat()
            
        # Add log level
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
            
        # Add request context if available
        if has_request_context():
            log_record['ip'] = request.remote_addr
            log_record['method'] = request.method
            log_record['url'] = request.url
            log_record['user_agent'] = request.user_agent.string
            
            # Add user ID if authenticated
            from flask_login import current_user
            if current_user and current_user.is_authenticated:
                log_record['user_id'] = current_user.userId

def setup_logging(app):
    """
    Configure application logging.
    
    Args:
        app: Flask application instance
    """
    # Ensure log directory exists
    log_dir = os.path.join(app.root_path, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create formatters
    json_formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    
    # Create handlers for different log levels
    info_handler = RotatingFileHandler(
        os.path.join(log_dir, 'info.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(json_formatter)
    
    error_handler = RotatingFileHandler(
        os.path.join(log_dir, 'error.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(json_formatter)
    
    security_handler = RotatingFileHandler(
        os.path.join(log_dir, 'security.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    security_handler.setLevel(logging.WARNING)
    security_handler.setFormatter(json_formatter)
    
    # Add handlers to app logger
    app.logger.addHandler(info_handler)
    app.logger.addHandler(error_handler)
    app.logger.addHandler(security_handler)
    
    # Set overall logging level
    app.logger.setLevel(logging.INFO)

def log_security_event(event_type, details, user_id=None):
    """
    Log a security-related event.
    
    Args:
        event_type (str): Type of security event (e.g., 'login_attempt', 'password_change')
        details (dict): Additional event details
        user_id (int, optional): ID of the user involved
    """
    if not current_app:
        return
        
    log_data = {
        'event_type': event_type,
        'details': details
    }
    
    if user_id:
        log_data['user_id'] = user_id
        
    if has_request_context():
        log_data['ip'] = request.remote_addr
        log_data['user_agent'] = request.user_agent.string
    
    current_app.logger.warning(f'Security Event: {json.dumps(log_data)}')
