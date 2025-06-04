
"""
Utility functions for handling notifications in the DreamHome Real Estate Portal.
Provides methods to create, retrieve, and manage user notifications.
"""
from flask import current_app
from models import db, Notification, User
from sqlalchemy import desc
from datetime import datetime

def create_notification(user_id, title, message, notification_type="system"):
    """
    Create a new notification for a user
    
    Args:
        user_id (int): The ID of the user to notify
        title (str): The notification title
        message (str): The notification message
        notification_type (str): Type of notification (default: "system")
        
    Returns:
        Notification: The created notification object
    """
    try:
        notification = Notification(
            userId=user_id,
            title=title,
            message=message,
            type=notification_type,
            isRead=False
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    except Exception as e:
        current_app.logger.error(f"Error creating notification: {str(e)}")
        db.session.rollback()
        return None

def mark_notification_as_read(notification_id):
    """
    Mark a notification as read
    
    Args:
        notification_id (int): The ID of the notification to mark as read
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        notification = db.session.get(Notification, notification_id)
        if notification:
            notification.isRead = True
            notification.read_at = db.func.now()
            db.session.commit()
            return True
        return False
    except Exception as e:
        current_app.logger.error(f"Error marking notification as read: {str(e)}")
        db.session.rollback()
        return False

def get_unread_notifications_count(user_id):
    """
    Get the number of unread notifications for a user
    
    Args:
        user_id (int): The ID of the user
        
    Returns:
        int: The number of unread notifications
    """
    try:
        return Notification.query.filter_by(userId=user_id, isRead=False).count()
    except Exception as e:
        current_app.logger.error(f"Error getting unread notification count: {str(e)}")
        return 0

def get_recent_notifications(user_id, limit=10):
    """
    Get recent notifications for a user
    
    Args:
        user_id (int): The ID of the user
        limit (int): Maximum number of notifications to return
        
    Returns:
        list: A list of notification objects
    """
    try:
        return Notification.query.filter_by(userId=user_id).order_by(
            desc(Notification.createdAt)
        ).limit(limit).all()
    except Exception as e:
        current_app.logger.error(f"Error getting recent notifications: {str(e)}")
        return []

def send_property_notification(property_id, title, message):
    """
    Send a notification to all users who have favorited a property
    
    Args:
        property_id (int): The ID of the property
        title (str): The notification title
        message (str): The notification message
        
    Returns:
        int: The number of notifications sent
    """
    # Implement this after adding favorites functionality
    pass
