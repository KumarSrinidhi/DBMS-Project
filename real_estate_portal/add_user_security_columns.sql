-- Add new security-related columns to Users table
ALTER TABLE Users
ADD COLUMN loginAttempts INT DEFAULT 0,
ADD COLUMN lastLoginAttempt DATETIME NULL,
ADD COLUMN lastPasswordChange DATETIME NULL,
ADD COLUMN passwordResetToken VARCHAR(100) NULL UNIQUE,
ADD COLUMN passwordResetExpires DATETIME NULL,
ADD COLUMN lastLogin DATETIME NULL,
ADD COLUMN lastLoginIP VARCHAR(45) NULL,
ADD COLUMN twoFactorEnabled BOOLEAN DEFAULT FALSE,
ADD COLUMN twoFactorSecret VARCHAR(32) NULL;
