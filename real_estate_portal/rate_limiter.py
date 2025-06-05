"""
Rate limiting implementation for DreamHome Real Estate Portal.
Provides decorators and utilities to prevent abuse of sensitive endpoints.
"""
from functools import wraps
from datetime import datetime, timedelta
from flask import request, abort, current_app
from redis import Redis
import time

class RateLimiter:
    """Rate limiting using Redis."""
    
    def __init__(self, redis_url=None):
        """
        Initialize rate limiter.
        
        Args:
            redis_url (str, optional): Redis connection URL
        """
        self.redis = Redis.from_url(redis_url) if redis_url else Redis()
        
    def is_rate_limited(self, key, limit, period):
        """
        Check if a key has exceeded its rate limit.
        
        Args:
            key (str): Unique identifier for the rate limit bucket
            limit (int): Maximum number of requests allowed
            period (int): Time period in seconds
            
        Returns:
            bool: True if rate limited, False otherwise
        """
        current = int(time.time())
        pipeline = self.redis.pipeline()
        
        # Add current timestamp to sorted set
        pipeline.zadd(key, {str(current): current})
        
        # Remove timestamps outside the window
        pipeline.zremrangebyscore(key, 0, current - period)
        
        # Count timestamps in the current window
        pipeline.zcard(key)
        
        # Set key expiration
        pipeline.expire(key, period)
        
        # Execute commands
        _, _, count, _ = pipeline.execute()
        
        return count > limit

def rate_limit(limit, period):
    """
    Decorator to apply rate limiting to routes.
    
    Args:
        limit (int): Maximum number of requests allowed
        period (int): Time period in seconds
        
    Usage:
        @app.route('/api/endpoint')
        @rate_limit(100, 3600)  # 100 requests per hour
        def api_endpoint():
            return 'API response'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Initialize rate limiter
            limiter = RateLimiter(current_app.config.get('RATELIMIT_STORAGE_URL'))
            
            # Get client identifier (IP address or user ID)
            if hasattr(request, 'user') and request.user.is_authenticated:
                key = f"rate_limit:{request.user.id}:{request.endpoint}"
            else:
                key = f"rate_limit:{request.remote_addr}:{request.endpoint}"
            
            # Check rate limit
            if limiter.is_rate_limited(key, limit, period):
                abort(429)  # Too Many Requests
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_rate_limit():
    """
    Special rate limiting for login attempts.
    Progressive delay based on number of failed attempts.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from models import User
            from flask_login import current_user
            
            if request.method == 'POST':
                username = request.form.get('username')
                user = User.query.filter_by(username=username).first()
                
                if user and user.loginAttempts >= 5:
                    # Calculate lockout time based on number of attempts
                    lockout_minutes = min(2 ** (user.loginAttempts - 5), 60)  # Max 60 minutes
                    if user.lastLoginAttempt and \
                       user.lastLoginAttempt + timedelta(minutes=lockout_minutes) > datetime.utcnow():
                        return abort(429)  # Too Many Requests
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
