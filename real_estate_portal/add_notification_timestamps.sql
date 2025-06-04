
/*
 * Notification system enhancement script
 * Adds read timestamp tracking to notifications and optimizes database queries
 * This script should be run after the initial database setup is complete
 */

-- Add read_at timestamp to track when notifications are read
ALTER TABLE Notifications 
ADD COLUMN read_at TIMESTAMP NULL;

-- Update the isRead status whenever read_at is set
-- This trigger is for MySQL/MariaDB
DELIMITER //
CREATE TRIGGER set_is_read_status
BEFORE UPDATE ON Notifications
FOR EACH ROW
BEGIN
    IF NEW.read_at IS NOT NULL AND OLD.read_at IS NULL THEN
        SET NEW.isRead = TRUE;
    END IF;
END//
DELIMITER ;

-- Create index for faster queries on unread notifications by user
CREATE INDEX idx_notifications_user_read 
ON Notifications(userId, isRead);

-- Create index for sorting notifications by creation date
CREATE INDEX idx_notifications_created 
ON Notifications(createdAt DESC);
