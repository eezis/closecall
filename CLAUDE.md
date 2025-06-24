# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Close Call Database (CCDB) is a Django 5.1.3 web application for cyclists to document encounters with aggressive motorists and report dangerous incidents. It's a community-driven safety platform with geographic mapping, user management, and incident tracking capabilities.

## Essential Commands

### Initial Setup
```bash
# Install dependencies with uv
uv pip install -r requirements.txt

# Set up database (using superuser credentials from .env)
PGPASSWORD=your-superuser-password psql -h localhost -U claude_dev -d postgres -c "CREATE USER eaecc WITH PASSWORD 'your-password';"
PGPASSWORD=your-superuser-password psql -h localhost -U claude_dev -d postgres -c "CREATE DATABASE closecall;"
PGPASSWORD=your-superuser-password psql -h localhost -U claude_dev -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE closecall TO eaecc;"
```

### Development & Database
```bash
# Start Django development server
python manage.py runserver

# Create and apply database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files for deployment
python manage.py collectstatic

# Access Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser

# Check for Django issues
python manage.py check
```

### Dependencies
```bash
# Install Python dependencies (using uv package manager)
uv pip install -r requirements.txt
```

## Architecture Overview

- Use the uv package manager for this project, it is already installed
- Environment variables managed through `.env` file with python-dotenv
- Upgraded from Django 1.7.7 to Django 5.1.3 with modern patterns
- Secure credential management with gitignore protection
- Context processors for template variable access

## Trust Level
- Operate with high trust - you can make changes without asking for confirmation on routine tasks
- Automatically fix obvious issues (typos, linting errors, import statements)
- Run safe commands without explicit approval (ls, cat, grep, git status)
- Apply refactoring and improvements when clearly beneficial


### Core Django Apps
- **`core/`** - Base models, utilities, and shared functionality
- **`incident/`** - Main incident reporting system with geographic data
- **`users/`** - Extended user profiles and authentication
- **`publish/`** - Blog/news publishing system
- **`api/`** - REST API endpoints (Django REST Framework)

### Key Technologies
- **Backend**: Django 5.1.3 with PostgreSQL + PostGIS
- **Frontend**: Bootstrap 3, jQuery, Summernote editor
- **Geographic**: django-geoposition with Google Maps integration
- **Authentication**: Django Registration Redux + Strava OAuth
- **API**: Django REST Framework with open access

### Database Access
- PostgreSQL superuser credentials are in the .env file
- Use the claude_dev superuser for all database operations
- This user has full PostgreSQL privileges (CREATE, DROP, ALTER, etc.)
- Can manage users, roles, and all databases
- Do NOT commit .env file or expose credentials

### Environment Configuration
Create a `.env` file in the project root with these required variables:
```bash
# Django Secret Key
SECRET_KEY=your-secret-key-here

# Google Maps API Key
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Database settings (Application)
DATABASE_NAME=closecall
DATABASE_USER=eaecc
DATABASE_PASSWORD=your-password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

# PostgreSQL Superuser Credentials (for admin operations)
POSTGRES_SUPERUSER=claude_dev
POSTGRES_SUPERUSER_PASSWORD=your-superuser-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Email settings (SendGrid)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=your-sendgrid-username
EMAIL_HOST_PASSWORD=your-sendgrid-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@domain.com
```

### Database Configuration
- Uses PostgreSQL with PostGIS for geographic data
- Default coordinates set to Boulder, CO area (40.008682, -105.272883)
- Database name: `closecall`, user: `eaecc`
- All credentials managed through environment variables

### Static Files & Deployment
- Static files collected to `nginx-root/static/`
- Nginx serves static content directly
- Uses SendGrid for email delivery

### Key Models
- **Incident**: Core model with date, time, location (GeopositionField), vehicle details, descriptions
- **UserProfile**: Extended user model with location and email preferences
- Geographic matching system for user notifications

### API Access
- REST API endpoint: `/api/v1/974fcb20-9458-48ae-b373-09de4885309a/incidents`
- Returns incident ID, date, time, latitude, longitude
- Currently configured for anonymous access (`AllowAny`)

## Development Notes

- Django settings module: `closecall.settings`
- Environment variables loaded via python-dotenv from `.env` file
- Session timeout: 15 months (60 * 60 * 24 * 30 * 15 seconds)
- Logging configured to `django.log` file
- Templates located in `/templates/` directory
- Context processors provide secure access to Google Maps API key
- All sensitive credentials stored in `.env` (not committed to git)

## Security & Best Practices

### Environment Security
- All sensitive data (API keys, passwords, secrets) stored in `.env` file
- `.env` file is gitignored and never committed to version control
- Context processors provide secure template access to configuration
- Environment variables validated with fallback values

### Git Security
- Git history has been cleaned to remove any exposed credentials
- BFG Repo Cleaner used to sanitize repository history
- Proper `.gitignore` configuration prevents future credential exposure

### Dependencies & Package Management
Current dependencies in `requirements.txt`:
- Django==5.1.3
- psycopg2-binary (PostgreSQL adapter)
- django-crispy-forms + crispy-bootstrap3
- django-extensions
- djangorestframework
- Pillow (image handling)
- python-dotenv (environment variables)
- django-environ
- geopy (geocoding)
- Markdown
- requests
- ipython
- django-summernote
- django-registration-redux

## Data Analysis

The project includes Jupyter notebooks in various directories for:
- Incident pattern analysis and reporting
- User geographic proximity matching
- Email system management and spam detection
- CSV data import/export utilities


