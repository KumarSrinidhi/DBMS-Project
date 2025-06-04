"""
Database maintenance script for DreamHome Real Estate Portal.
Fixes various database issues including auto-increment problems and column definitions.
Run this script when database structure needs to be corrected without full migration.
"""
from app import app, db
import sqlalchemy

def fix_property_table():
    """
    Fix the Property table by ensuring propertyId is set as auto-increment
    """
    with app.app_context():
        conn = db.engine.connect()
        
        try:
            # Check current state of the column
            result = conn.execute(sqlalchemy.text("""
                SELECT COLUMN_NAME, EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'Property' AND COLUMN_NAME = 'propertyId'
            """))
            row = result.fetchone()
            print("Current propertyId column configuration:")
            print(f"Column: {row[0]}, Extra: {row[1]}")
            
            # If AUTO_INCREMENT is not set, modify the column
            if 'auto_increment' not in row[1].lower():
                print("\nModifying propertyId column to add AUTO_INCREMENT...")
                
                # Disable foreign key checks before modifying the column
                print("Temporarily disabling foreign key checks...")
                conn.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 0;"))
                
                # Modify the column
                conn.execute(sqlalchemy.text("""
                    ALTER TABLE `Property` MODIFY COLUMN `propertyId` INT AUTO_INCREMENT
                """))
                
                # Re-enable foreign key checks
                print("Re-enabling foreign key checks...")
                conn.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 1;"))
                
                conn.commit()
                print("Column modified successfully!")
            else:
                print("\nThe propertyId column already has AUTO_INCREMENT. No changes needed.")
                
            # Verify the change
            result = conn.execute(sqlalchemy.text("""
                SELECT COLUMN_NAME, EXTRA
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'Property' AND COLUMN_NAME = 'propertyId'
            """))
            row = result.fetchone()
            print("\nVerification - current propertyId column configuration:")
            print(f"Column: {row[0]}, Extra: {row[1]}")
            
            return True
            
        except Exception as e:
            print(f"Error fixing Property table: {str(e)}")
            # Make sure to re-enable foreign key checks even if there's an error
            try:
                conn.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 1;"))
                conn.commit()
            except:
                pass
            return False
        finally:
            conn.close()

if __name__ == "__main__":
    print("Starting database fix script...")
    result = fix_property_table()
    if result:
        print("\nDatabase fix completed successfully. You should now be able to add properties.")
    else:
        print("\nDatabase fix encountered an error. Please check the error messages above.")