"""
Utility script to update property image paths in the database.
Synchronizes the database image records with actual files on disk.
Run this script after migration or when file paths are out of sync.
"""
import os
import sys
from app import app, db
from models import Property, PropertyImages

def update_property_image_paths():
    """
    Updates the database with correct image paths that match the files on disk.
    This script resolves issues where image paths in the database don't match actual files.
    """
    print("Starting image path update process...")
    
    # Get all properties with images
    properties = Property.query.all()
    properties_updated = 0
    images_updated = 0
    
    for property in properties:
        print(f"\nChecking property ID: {property.propertyId}")
        property_folder = os.path.join(app.root_path, 'static', 'images', 'properties', str(property.propertyId))
        
        # Check if property folder exists
        if not os.path.exists(property_folder):
            print(f"  Warning: Folder for property {property.propertyId} doesn't exist at {property_folder}")
            continue
        
        # List all image files in the property folder
        actual_files = []
        try:
            actual_files = [f for f in os.listdir(property_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"  Found {len(actual_files)} image files on disk: {', '.join(actual_files)}")
        except Exception as e:
            print(f"  Error listing files in {property_folder}: {str(e)}")
            continue
            
        if not actual_files:
            print(f"  No image files found for property {property.propertyId}")
            continue
            
        # Get database records for this property's images
        db_images = PropertyImages.query.filter_by(propertyId=property.propertyId).all()
        print(f"  Found {len(db_images)} image records in database")
        
        if not db_images:
            print(f"  Creating new image records for property {property.propertyId}")
            # Create new image records for each file
            for idx, filename in enumerate(actual_files):
                new_image = PropertyImages(
                    propertyId=property.propertyId,
                    imageURL=f'/static/images/properties/{property.propertyId}/{filename}',
                    isPrimary=(idx == 0)  # First image is primary
                )
                db.session.add(new_image)
                images_updated += 1
            properties_updated += 1
        else:
            # Check each database record and update if needed
            existing_count = len(db_images)
            file_count = len(actual_files)
            
            # Update existing records to match files
            for idx, image in enumerate(db_images):
                if idx < file_count:
                    # Get filename from the image URL
                    old_path = image.imageURL
                    filename = actual_files[idx]
                    new_path = f'/static/images/properties/{property.propertyId}/{filename}'
                    
                    # Update if paths don't match
                    if old_path != new_path:
                        print(f"  Updating image {image.imageId}: {old_path} -> {new_path}")
                        image.imageURL = new_path
                        images_updated += 1
                        
            # Add new records for additional files
            if file_count > existing_count:
                for idx in range(existing_count, file_count):
                    filename = actual_files[idx]
                    new_image = PropertyImages(
                        propertyId=property.propertyId,
                        imageURL=f'/static/images/properties/{property.propertyId}/{filename}',
                        isPrimary=False
                    )
                    print(f"  Adding new image record: {new_image.imageURL}")
                    db.session.add(new_image)
                    images_updated += 1
                    
            if images_updated > 0:
                properties_updated += 1
    
    # Commit changes
    try:
        db.session.commit()
        print(f"\nUpdate complete! Updated {images_updated} images across {properties_updated} properties.")
    except Exception as e:
        db.session.rollback()
        print(f"\nError committing changes to database: {str(e)}")
        return False
        
    return True

def verify_image_paths():
    """
    Verifies that all image paths in the database point to existing files.
    """
    print("\nVerifying image paths after update...")
    
    images = PropertyImages.query.all()
    valid_count = 0
    invalid_count = 0
    
    for image in images:
        # Convert URL to filesystem path
        if image.imageURL.startswith('/'):
            fs_path = os.path.join(app.root_path, image.imageURL[1:])
        else:
            fs_path = os.path.join(app.root_path, image.imageURL)
            
        if os.path.exists(fs_path):
            valid_count += 1
        else:
            invalid_count += 1
            print(f"Invalid path: {image.imageURL} (ID: {image.imageId}, Property: {image.propertyId})")
    
    print(f"\nVerification complete: {valid_count} valid paths, {invalid_count} invalid paths")

if __name__ == "__main__":
    with app.app_context():
        print("=== Property Image Path Update Tool ===")
        print("This script will update image paths in the database to match actual files on disk.")
        
        # Ask for confirmation before proceeding
        if input("Do you want to proceed with the update? (y/n): ").lower() != 'y':
            print("Update cancelled.")
            sys.exit(0)
            
        success = update_property_image_paths()
        
        if success:
            verify_image_paths()
        
        print("\nScript execution complete.")