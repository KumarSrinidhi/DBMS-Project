# DreamHome Real Estate Portal

A comprehensive web application for real estate property listing, searching, and management.

## Features

- Property listing and searching with advanced filters
- User roles: Admin, Agent, Buyer, and Seller
- User authentication and profile management
- Property details with images and amenities
- Administrative dashboard for user and property management
- Interactive tools: Loan calculator, property valuation, comparison

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: Bootstrap 5, jQuery, Leaflet.js
- **Authentication**: Flask-Login

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - `SECRET_KEY` - For session security
   - `DATABASE_URL` - MySQL connection string

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

## Project Structure

- `app.py`: Main application file with routes and controller logic
- `models.py`: Database models and schema definition
- `config.py`: Application configuration settings
- `forms.py`: Form definitions using Flask-WTF
- `templates/`: HTML templates for the web interface
- `static/`: Static assets (CSS, JS, images)
- `maintenance.py`: Maintenance mode functionality
- `notification_utils.py`: Notification system utilities

## Maintenance Scripts

- `fix_database.py`: Script to fix database issues
- `fix_passwords.py`: Script to reset/fix user passwords
- `update_image_paths.py`: Utility to correct image path references

## License

Copyright © 2025 DreamHome Real Estate Portal