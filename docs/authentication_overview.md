# Authentication Overview - Close Call Database

**Last Updated: November 11, 2025**

## Overview

The Close Call Database supports two authentication methods:
1. **Traditional Registration** - Username/email/password registration
2. **Strava OAuth** - Social login via Strava (cyclist fitness app)

## Traditional Registration Flow

### Registration Process

1. **User visits** `/accounts/register/`
2. **Fills form** with:
   - Username
   - Email address
   - Password (minimum 6 characters)
   - First name
   - Last name
   - City, State, Country
   - Zipcode (optional)

3. **Django Registration Redux** handles:
   - User creation (Django User model)
   - UserProfile creation (extended profile)
   - Sends activation email via SendGrid
   - User must click activation link within 7 days

4. **Email Activation**:
   - Template: `templates/registration/activation_email.html`
   - Contains activation link with unique key
   - Valid for `ACCOUNT_ACTIVATION_DAYS = 7` days

5. **After Activation**:
   - User is automatically logged in
   - UserProfile is geocoded based on location
   - User can receive incident notifications for their area

### Login Process

1. **User visits** `/accounts/login/`
2. **Enters** username and password
3. **Django auth** validates credentials
4. **Redirects to** homepage or next URL

### Password Reset

1. **User visits** `/accounts/password/reset/`
2. **Enters** email address
3. **System sends** reset link via SendGrid
4. **User clicks** link and sets new password

## Strava OAuth Flow

### Why Strava?

- Primary user base is cyclists
- Strava is the leading cycling/fitness app
- Reduces friction for user registration
- Provides athlete profile data

### Registration Process (Two-Step)

**Step 1: Strava Authorization**

1. **User clicks** "Register with Strava" button
2. **Redirects to** Strava OAuth:
   ```
   https://www.strava.com/oauth/authorize?
   client_id=3163&
   response_type=code&
   redirect_uri=https://closecalldatabase.com/strava-registration&
   scope=read&
   state=&
   approval_prompt=force
   ```

3. **User authorizes** on Strava's site
4. **Strava redirects** back with authorization code

**Step 2: Email Collection** (Added November 2025)

Since Strava removed email from their API response in 2019, we now collect it separately:

1. **System receives** Strava callback at `/strava-registration`
2. **Exchanges code** for access token and athlete data:
   - Athlete ID
   - First name
   - Last name
   - City, State, Country
   - Profile picture URL

3. **Stores in session**:
   - `request.session['strava_athlete']` - athlete data
   - `request.session['strava_access_token']` - for future API calls

4. **Redirects to** `/strava-complete-registration`
5. **Shows form** with:
   - Pre-filled Strava athlete info (read-only display)
   - Email address field (required)
   - Professional UI with Strava branding

6. **On submission**:
   - Creates Django User with username: `{firstname} {lastname}-{strava_id}`
   - Creates UserProfile with Strava data
   - Sets `created_with = "Strava={strava_id}"`
   - Stores OAuth data for future use
   - Automatically logs user in
   - Clears session data

### Existing Strava User Login

1. **User clicks** "Log in with Strava"
2. **Same OAuth flow** as registration
3. **System checks** if Strava ID exists in database
4. **If exists**: Logs user in automatically
5. **If not exists**: Proceeds with registration flow

## Security Features

### CSRF Protection

- Django's built-in CSRF middleware
- Custom `AntiCSRFBypassMiddleware` that:
  - Tracks GET→POST patterns
  - Blocks requests without referers
  - Rate limits suspicious attempts
  - Blocks clients after 3 violations

### Registration Logging

All registration attempts are logged with:
- IP address (considering X-Forwarded-For headers)
- Email address
- Username
- User agent
- Success/failure status
- Error details

Logs are written to:
- `logs/users.log` - User events
- `logs/security.log` - Security events

### Password Requirements

Enforced via Django validators:
- Minimum 6 characters
- Not entirely numeric
- Not too similar to username
- Not a common password

## Database Models

### User Model
- Standard Django `User` model
- Username format for Strava: `{firstname} {lastname}-{strava_id}`

### UserProfile Model
```python
class UserProfile(BaseFields):
    user = OneToOneField(User)
    first = CharField(max_length=50)
    last = CharField(max_length=50)
    city = CharField(max_length=120)
    state = CharField(max_length=50)
    country = CharField(max_length=80)
    zipcode = CharField(max_length=30, blank=True)
    email_incidents = BooleanField(default=True)
    position = CharField(max_length=80)  # Geocoded lat/lon
    created_with = CharField(max_length=250)  # "Strava=12345" or None
    oauth_data = TextField(blank=True)  # JSON OAuth response
    can_blog = BooleanField(default=False)
```

## Configuration

### Settings (`closecall/settings.py`)

```python
# Session duration
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 * 15  # 15 months

# Authentication redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Registration settings
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

# Email configuration
EMAIL_HOST = 'smtp.sendgrid.net'
DEFAULT_FROM_EMAIL = 'closecalldatabase@gmail.com'
```

### URLs

- `/accounts/register/` - Traditional registration
- `/accounts/login/` - Traditional login
- `/accounts/logout/` - Logout (POST only)
- `/accounts/password/reset/` - Password reset
- `/get-strava-login` - Initiate Strava OAuth
- `/strava-registration` - Strava OAuth callback
- `/strava-complete-registration` - Email collection for Strava users

## Recent Changes

### November 2025 - Fixed Strava Registration

**Problem**: Strava registration broken since 2019 when Strava removed email from API response

**Solution**: Implemented two-step registration:
1. Strava OAuth for athlete data
2. Email collection form

**Impact**:
- 4 successful Strava registrations in first week after fix
- 72% of 16,039 users registered via Strava

### Django 5 Compatibility

- Removed deprecated `{% load url from future %}` template tags
- Fixed `User.last_login` null constraint issues
- Updated to django-registration-redux for Django 5 support

## Statistics (as of November 2025)

- **Total users**: 16,039
- **Strava registrations**: 11,655 (72%)
- **Traditional registrations**: 4,384 (27%)
- **Recent activity**: All new registrations are via Strava

## Monitoring

Check registration status:
```bash
python registration_report.py
```

This shows:
- Overall registration statistics
- Recent registration activity (7, 30, 365 days)
- Breakdown by registration type
- Details of most recent Strava registration