"""
Custom decorators for DreamHome Real Estate Portal.
Provides reusable decorators for route protection and access control.
"""
from functools import wraps
from flask import abort
from flask_login import current_user
from models import Roles

def roles_required(*role_ids):
    """
    Decorator to restrict route access to specific roles.
    
    Args:
        *role_ids: Variable number of role IDs that are allowed to access the route
        
    Usage:
        @app.route('/admin')
        @roles_required(Roles.ADMIN)
        def admin_dashboard():
            return 'Admin only!'
            
        @app.route('/property/add')
        @roles_required(Roles.ADMIN, Roles.AGENT, Roles.SELLER)
        def add_property():
            return 'Add property form'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.roleId not in role_ids:
                abort(403)
            if current_user.isBanned or not current_user.isActive:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """
    Decorator to restrict route access to admin users only.
    """
    return roles_required(Roles.ADMIN)(f)

def active_user_required(f):
    """
    Decorator to ensure user is active and not banned.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.isBanned or not current_user.isActive:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
