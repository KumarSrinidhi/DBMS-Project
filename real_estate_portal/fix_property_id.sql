/*
 * Fix for the Property table primary key issue
 * This script modifies the Property table to ensure propertyId is auto-incrementing
 * Run this after creating the initial database structure if auto-increment is not working
 */

-- First, check if the propertyId column already has AUTO_INCREMENT
SELECT COLUMN_NAME, EXTRA
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Property' AND COLUMN_NAME = 'propertyId';

-- If it doesn't have AUTO_INCREMENT, modify the column
ALTER TABLE `Property` MODIFY COLUMN `propertyId` INT AUTO_INCREMENT;

-- Verify that the change was successful
SELECT COLUMN_NAME, EXTRA
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Property' AND COLUMN_NAME = 'propertyId';