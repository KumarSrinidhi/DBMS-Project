#!/usr/bin/env python3
"""
Debug script to test upload functionality
"""

import requests
import os
from PIL import Image
import io

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_routes():
    """Test if the upload routes are accessible"""
    base_url = "http://localhost:5000"
    
    routes_to_test = [
        "/",
        "/login",
        "/upload/temp",  # This should return 405 Method Not Allowed for GET
        "/upload/1"      # This should return 405 Method Not Allowed for GET
    ]
    
    print("Testing route accessibility...")
    for route in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5)
            print(f"GET {route}: Status {response.status_code}")
            if response.status_code == 405:
                print(f"  ✓ Route exists (Method Not Allowed is expected for upload routes)")
            elif response.status_code == 200:
                print(f"  ✓ Route accessible")
            elif response.status_code == 404:
                print(f"  ✗ Route not found")
            else:
                print(f"  ? Unexpected status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error accessing {route}: {e}")

def test_upload_without_auth():
    """Test upload without authentication (should fail)"""
    base_url = "http://localhost:5000"
    
    print("\nTesting upload without authentication...")
    
    # Create test image
    test_image = create_test_image()
    
    files = {'file': ('test.jpg', test_image, 'image/jpeg')}
    
    try:
        response = requests.post(f"{base_url}/upload/temp", files=files, timeout=10)
        print(f"POST /upload/temp: Status {response.status_code}")
        if response.status_code == 401 or response.status_code == 302:
            print("  ✓ Correctly redirected/rejected (authentication required)")
        else:
            print(f"  Response: {response.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error: {e}")

if __name__ == "__main__":
    print("=== Upload Route Debug Test ===")
    print()
    
    test_routes()
    test_upload_without_auth()
    
    print()
    print("=== Next Steps ===")
    print("1. If routes are accessible, the issue might be with authentication")
    print("2. Check browser console for JavaScript errors")
    print("3. Check if Flask app is running on the correct port")
    print("4. Try testing with authentication (login first)")
