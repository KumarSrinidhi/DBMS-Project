-- Add new columns to UserDocuments table for enhanced document handling
ALTER TABLE UserDocuments
ADD COLUMN original_filename VARCHAR(255) NULL,
ADD COLUMN file_size INT NULL,
ADD COLUMN mime_type VARCHAR(100) NULL,
ADD COLUMN upload_date DATETIME NULL,
ADD COLUMN verified_by INT NULL,
ADD COLUMN verification_date DATETIME NULL,
ADD COLUMN rejection_reason VARCHAR(500) NULL,
ADD CONSTRAINT fk_verified_by FOREIGN KEY (verified_by) REFERENCES Users(userId) ON DELETE SET NULL;

-- Update the upload_date with the existing uploaded_at value for backward compatibility
UPDATE UserDocuments SET upload_date = uploaded_at WHERE upload_date IS NULL;
