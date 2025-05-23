
from flask import Flask, render_template, request, current_app, redirect, url_for
from functools import wraps
import os
import time

class MaintenanceMode:
    """
    Middleware to handle maintenance mode for the application.
    When enabled, all requests are redirected to a maintenance page.
    """
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
            
    def init_app(self, app):
        app.config.setdefault('MAINTENANCE_MODE', False)
        app.config.setdefault('MAINTENANCE_BYPASS_IPS', [])
        app.config.setdefault('MAINTENANCE_BYPASS_KEY', None)
        app.config.setdefault('MAINTENANCE_TEMPLATE', 'maintenance/maintenance.html')
        app.config.setdefault('MAINTENANCE_BYPASS_QUERY_KEY', '_bypass_maintenance')
        
        app.before_request(self._check_maintenance)
        
        # Add command to toggle maintenance mode
        @app.cli.command('maintenance')
        def maintenance_command():
            """Toggle maintenance mode on/off"""
            mode_file = os.path.join(app.root_path, 'maintenance_mode')
            if os.path.exists(mode_file):
                os.remove(mode_file)
                print("Maintenance mode: OFF")
            else:
                with open(mode_file, 'w') as f:
                    f.write(str(int(time.time())))
                print("Maintenance mode: ON")
                
    def _check_maintenance(self):
        """Check if the application is in maintenance mode and handle the request accordingly"""
        # Skip for static files
        if request.path.startswith('/static/'):
            return None
            
        # Check if maintenance mode is enabled
        in_maintenance = self._is_maintenance_mode_enabled()
        if in_maintenance and not self._can_bypass_maintenance():
            return render_template(current_app.config['MAINTENANCE_TEMPLATE']), 503
        
    def _is_maintenance_mode_enabled(self):
        """Check if maintenance mode is enabled"""
        # Check from config first
        if current_app.config['MAINTENANCE_MODE']:
            return True
            
        # Check from file (for persistence across restarts)
        mode_file = os.path.join(current_app.root_path, 'maintenance_mode')
        if os.path.exists(mode_file):
            return True
            
        return False
        
    def _can_bypass_maintenance(self):
        """Check if the current request can bypass maintenance mode"""
        # Allow specific IPs to bypass
        client_ip = request.remote_addr
        if client_ip in current_app.config['MAINTENANCE_BYPASS_IPS']:
            return True
            
        # Allow requests with the bypass key in query string
        bypass_key = current_app.config['MAINTENANCE_BYPASS_KEY']
        if bypass_key and request.args.get(current_app.config['MAINTENANCE_BYPASS_QUERY_KEY']) == bypass_key:
            return True
            
        return False
        
# Create decorator to exempt specific views from maintenance mode
def maintenance_exempt(f):
    """Decorator to exempt a view from maintenance mode"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    setattr(decorated_function, '_maintenance_exempt', True)
    return decorated_function
