# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Close Call Database (CCDB) is a Django 1.7.7 web application for cyclists to document encounters with aggressive motorists and report dangerous incidents. It's a community-driven safety platform with geographic mapping, user management, and incident tracking capabilities.

## Essential Commands

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
```

### Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt
```

## Architecture Overview

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
- **Backend**: Django 1.7.7 with PostgreSQL + PostGIS
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

### Database Configuration
- Uses PostgreSQL with PostGIS for geographic data
- Default coordinates set to Boulder, CO area (40.008682, -105.272883)
- Database name: `closecall`, user: `eaecc`

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
- Session timeout: 15 months (60 * 60 * 24 * 30 * 15 seconds)
- Logging configured to `django-errors.log` file
- Templates located in `/templates/` directory
- Custom geographic positioning in `/geoposition/` app

## Data Analysis

The project includes Jupyter notebooks in various directories for:
- Incident pattern analysis and reporting
- User geographic proximity matching
- Email system management and spam detection
- CSV data import/export utilities


