# Authentication Overview - Close Call Database

**Last Updated: November 12, 2025**

## Overview

The Close Call Database supports two authentication methods:
1. **Traditional Registration** - Username/email/password registration
2. **Strava OAuth** - Social login via Strava (cyclist fitness app)

## Traditional Registration Flow

### Registration Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRADITIONAL REGISTRATION                      │
└─────────────────────────────────────────────────────────────────┘

1. User Action: Navigate to /accounts/register/
   ↓
2. System: Display registration form (templates/registration/registration_form.html)
   - Username (required, unique)
   - Email (required, unique)
   - Password (required, min 6 chars)
   - Password confirmation (must match)
   ↓
3. User Action: Submit form
   ↓
4. System: Validate form data
   - Check username not taken
   - Check email not registered
   - Validate password strength
   - Verify passwords match
   ↓
5. System: Create User account
   - Status: INACTIVE (is_active=False)
   - Generate activation key
   - Set expiration (7 days)
   - **Auto-create UserProfile** (via post_save signal using transaction.on_commit())
   ↓
6. System: Send activation email
   - To: User's email
   - Template: templates/registration/activation_email.txt
   - Contains: Activation link with unique key
   - Via: SendGrid SMTP
   ↓
7. System: Show confirmation page
   - Template: templates/registration/registration_complete.html
   - Message: "Check your email for activation link"
   ↓
8. User Action: Click activation link in email
   - URL: /accounts/activate/<activation_key>/
   ↓
9. System: Validate activation
   - Check key exists
   - Check not expired (< 7 days)
   - Activate user (is_active=True)
   ↓
10. System: Auto-login user (REGISTRATION_AUTO_LOGIN=True)
    ↓
11. System: Redirect to update user profile (profile already exists from step 5)
    - URL: /create-user-profile/
    ↓
12. User Action: Fill profile form
    - First name
    - Last name
    - City, State, Country
    - Email notification preferences
    ↓
13. System: Update UserProfile
    - Profile already created automatically in step 5
    - Update with user-provided details
    - Geocode location → position field
    - Save updated profile
    ↓
14. System: User fully registered and logged in
    - Redirect to homepage
    - User can now report incidents
    - User can receive location-based alerts
```

### Login Process Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        LOGIN PROCESS                             │
└─────────────────────────────────────────────────────────────────┘

1. User Action: Navigate to /accounts/login/
   ↓
2. System: Display login form (templates/registration/login.html)
   - Username field
   - Password field
   ↓
3. User Action: Submit credentials
   ↓
4. System: Authenticate
   - Query User.objects.get(username=username)
   - Verify password hash matches
   - Check is_active=True
   ↓
5. Success Path:
   - Create session
   - Set session cookie (15 month expiry)
   - Redirect to '/' or 'next' URL
   ↓
6. Failure Path:
   - Display error: "Invalid username or password"
   - Re-show login form
```

### Password Reset Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PASSWORD RESET                               │
└─────────────────────────────────────────────────────────────────┘

1. User Action: Click "Forgot Password?" on login page
   ↓
2. System: Show password reset form (/accounts/password/reset/)
   ↓
3. User Action: Enter email address
   ↓
4. System: Send reset email
   - Generate password reset token
   - Send email via SendGrid
   - Contains unique reset link
   ↓
5. User Action: Click link in email
   ↓
6. System: Show password reset form
   ↓
7. User Action: Enter new password (twice)
   ↓
8. System: Update password
   - Hash new password
   - Save to database
   - Invalidate reset token
   ↓
9. System: Redirect to login page
   - Show success message
```

### Key Implementation Details

**Django Registration Redux Handles:**
- User account creation
- Activation key generation and validation
- Email sending
- Auto-login after activation

**Signal Handlers (Django 5.1 Best Practices):**
- **Automatic UserProfile creation** via `post_save` signal on User model
- Uses `transaction.on_commit()` to avoid race conditions
- Only creates profile if one doesn't exist (Strava flow handles its own)
- Logs all profile creation attempts

**Application Handles:**
- UserProfile updates (profile auto-created by signal)
- Location geocoding
- Incident notification preferences

**Database State Transitions:**
```
[No Account]
    → Registration Form Submitted
        → User Created (is_active=False)
            → UserProfile Auto-Created (signal handler)
                → Email Sent
                    → User Clicks Activation Link
                        → User Activated (is_active=True)
                            → Auto-Login
                                → Profile Updated (user fills form)
                                    → [Fully Registered]
```

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
   - Creates or re-uses a Django `User` via `get_or_create_user()` which first looks up by email before falling back to username collisions
   - Signal handler auto-creates blank UserProfile (via transaction.on_commit())
   - View updates UserProfile with Strava data (race condition handled)
   - Sets `created_with = "Strava={athlete_id}"` (canonical casing; legacy `strava-<id>` is still parsed)
   - Stores OAuth data in `oauth_data` field for future use
   - Automatically logs user in
   - Clears session data

**Race Condition Prevention (Django 5.1 Best Practice):**
- Signal handler uses `transaction.on_commit()` to defer profile creation
- Strava view checks if profile exists before creating
- If profile exists (from signal), updates it with Strava data
- If profile doesn't exist, creates new one
- Prevents duplicate key errors that occurred in earlier versions

### Existing Strava User Login

1. **User clicks** "Log in with Strava"
   - Frontend dims the Strava button and shows a “Redirecting to Strava…” toast centered on the page so the cyclist knows the redirect is in progress.
2. **Same OAuth flow** as registration
3. **Server-side lookup order**:
   - `get_user_by_strava_id()` finds the canonical account by athlete ID (handles legacy `created_with` formats)
   - Duplicate emails are handled gracefully by preferring the user whose profile already records the matching Strava ID, falling back to the most recently active account only if needed
4. **If match exists**: Logs user in automatically
5. **If not exists**: Proceeds with registration flow (email collection)

### Observability & Logging

- All key Strava events (`/get-strava-login`, callback, token exchange, email collection) log through the dedicated `core.strava` logger which writes to `logs/strava.log`.
- The Strava view always emits INFO logs detailing the athlete ID, IP, and branch taken (new vs returning).
- Duplicate-email resolution logs at INFO level without emailing so repeated Strava logins do not generate alert noise.

## Security Features

### CSRF Protection

- Django's built-in CSRF middleware
- Custom `AntiCSRFBypassMiddleware` that:
  - Tracks GET→POST patterns
  - Blocks requests without referers
  - Rate limits suspicious attempts
  - Blocks clients after 3 violations

### Spam Protection

**Contact Form Honeypot:**
- Hidden "website" field catches bots (hidden via CSS)
- Legitimate users never see or fill this field
- Bots automatically fill all form fields
- Submissions with filled website field are rejected (403 Forbidden)
- Logged but no email alerts sent

**Content-Based Spam Detection:**
- URL detection (http://, https://, www.)
- E-commerce keywords (% off, free shipping, limited time, etc.)
- Banned IP tracking
- All spam attempts logged to `django.log`

### Registration and Error Logging

All registration attempts and errors are logged with:
- IP address (considering X-Forwarded-For headers)
- Email address
- Username
- User agent
- Success/failure status
- Error details and stack traces

**Improved Logging (November 2025):**
- `safe_print()` function now writes to log files (not just console/email)
- Critical errors logged as ERROR level
- Normal activity logged as INFO level
- All logs persisted to disk for observability

Logs are written to:
- `logs/django.log` - All application activity (main log file)
- `logs/users.log` - User-specific events
- `logs/security.log` - Security events (CSRF, suspicious activity)
- `logs/errors.log` - Error-level events only

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
# Timezone (Mountain Time - Denver)
TIME_ZONE = 'America/Denver'
USE_TZ = True

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

### November 12, 2025 - Signal Handler Improvements & Race Condition Fix

**Problem**:
1. Race condition between signal handler and Strava view causing duplicate profile errors
2. Users without profiles not being tracked (8,477 orphaned accounts)
3. Critical errors only sent via email, not logged to files

**Solution**:
1. **Implemented Django 5.1 best practices** - Signal handlers use `transaction.on_commit()` to avoid race conditions
2. **Automatic profile creation** - Traditional registration now auto-creates profiles via signals
3. **Strava view race condition fix** - Checks if profile exists, updates instead of creating duplicate
4. **Improved logging** - `safe_print()` now writes to log files for observability
5. **Spam protection** - Honeypot field on contact form, email notifications disabled for spam
6. **Timezone fix** - Changed from UTC to America/Denver for accurate timestamps

**Impact**:
- Eliminated duplicate profile creation errors
- All new registrations automatically get profiles
- Critical errors now visible in logs (not just email)
- Spam blocked silently (9 attempts caught first night)

### November 2025 - Fixed Strava Registration

**Problem**: Strava registration broken since 2019 when Strava removed email from API response

**Solution**: Implemented two-step registration:
1. Strava OAuth for athlete data
2. Email collection form

**Impact**:
- 4 successful Strava registrations in first week after fix
- 72% of 16,039 users registered via Strava
- One failed registration (Sung Ho Yang) due to race condition (fixed Nov 12)

### Django 5 Compatibility

- Removed deprecated `{% load url from future %}` template tags
- Fixed `User.last_login` null constraint issues
- Updated to django-registration-redux for Django 5 support

## Statistics (as of November 2025)

- **Total users**: 16,039
- **Strava registrations**: 11,655 (72%)
- **Traditional registrations**: 4,384 (27%)
- **Recent activity**: All new registrations are via Strava

## Testing

### Running Authentication Tests

Comprehensive test suite for traditional authentication flow:

```bash
# Run all authentication tests
python manage.py test tests.test_authentication

# Run specific test class
python manage.py test tests.test_authentication.RegistrationTests
python manage.py test tests.test_authentication.LoginTests
python manage.py test tests.test_authentication.ActivationTests

# Run specific test
python manage.py test tests.test_authentication.RegistrationTests.test_successful_registration

# Run with verbose output
python manage.py test tests.test_authentication --verbosity=2
```

### Test Coverage

The authentication test suite covers:

**Registration Tests:**
- ✓ Successful registration
- ✓ Duplicate username rejection
- ✓ Duplicate email rejection
- ✓ Password mismatch detection
- ✓ Weak password rejection
- ✓ Invalid email format
- ✓ Missing required fields

**Activation Tests:**
- ✓ Valid activation key
- ✓ Invalid activation key
- ✓ Expired activation key (> 7 days)
- ✓ Auto-login after activation

**Login Tests:**
- ✓ Successful login
- ✓ Invalid username
- ✓ Invalid password
- ✓ Inactive user (not activated)
- ✓ Case-sensitive username
- ✓ Login redirect to 'next' parameter

**Password Reset Tests:**
- ✓ Reset email sent for valid email
- ✓ No information disclosure for invalid email

**UserProfile Tests:**
- ✓ Profile auto-creation via signals
- ✓ Profile update (not duplicate creation)
- ✓ Login required for profile
- ✓ One profile per user constraint

**Integration Tests:**
- ✓ Complete registration flow (registration → activation → auto-profile → profile update)

**Security Tests:**
- ✓ Passwords hashed (never plaintext)
- ✓ CSRF protection on forms
- ✓ Session creation on login

### Test Database

**Important**: Tests that involve signal handlers with `transaction.on_commit()` must use `TransactionTestCase` instead of `TestCase`. This is because:
- `TestCase` wraps each test in a database transaction that's rolled back
- `transaction.on_commit()` callbacks never fire with rolled-back transactions
- `TransactionTestCase` actually commits to the test database

Tests use a temporary PostgreSQL database. Django handles test database creation and teardown automatically.

**Test Execution Notes:**
- Most tests use `TestCase` (fast, transactional rollback)
- UserProfile and Integration tests use `TransactionTestCase` (slower, requires actual commits)
- Current pass rate: 26/30 tests (87%) - 4 test isolation issues being addressed

## Monitoring

Check registration status:
```bash
python registration_report.py
```

This shows:
- Overall registration statistics (by registration type)
- Recent registration activity (7, 30, 365 days)
- Breakdown by Strava vs Traditional registration
- **Orphaned accounts** - Users without profiles (inactive/never activated)
- Details of most recent Strava and Traditional registrations
- Yearly breakdown of orphaned accounts

**Orphaned Account Tracking** (added November 12, 2025):
- Shows users who registered but never completed profile creation
- Distinguishes active vs inactive (email never verified)
- Helps identify registration issues
- Most orphaned accounts are spam/bots (inactive)
- Auto-profile creation eliminates new orphaned accounts

## Technical Implementation Details

### Signal Handler Implementation

**File**: `users/signals.py`

The signal handler follows Django 5.1 best practices:

```python
@receiver(post_save, sender=User)
def create_user_profile_on_registration(sender, instance, created, **kwargs):
    """Auto-create UserProfile using transaction.on_commit()"""
    if created:
        def create_profile_if_needed():
            try:
                user = User.objects.get(pk=instance.pk)
                if not hasattr(user, 'profile'):
                    UserProfile.objects.create(
                        user=user,
                        first=user.first_name or '',
                        last=user.last_name or '',
                        created_with='Traditional Registration'
                    )
                    logger.info(f"AUTO-CREATED UserProfile for: {user.username}")
            except User.DoesNotExist:
                logger.warning(f"User {instance.pk} rolled back")
            except Exception as e:
                logger.error(f"ERROR creating profile: {str(e)}")

        transaction.on_commit(create_profile_if_needed)
```

**Key Features:**
- Uses `transaction.on_commit()` to defer execution until after User is committed
- Refreshes user from database to ensure latest state
- Checks if profile already exists (Strava may have created it)
- Gracefully handles transaction rollbacks
- Comprehensive error logging

### Files Modified (November 12, 2025)

**Signal Handler:**
- `users/signals.py` - Added transaction.on_commit() wrapper

**Strava Registration:**
- `core/views.py` (strava_complete_registration) - Check/update existing profile instead of always creating

**Logging:**
- `core/views.py` (safe_print function) - Write to log files, not just console/email

**Spam Protection:**
- `core/models.py` (UserInput) - Added honeypot 'website' field
- `core/views.py` (CreateUserInput) - Honeypot validation, disabled email alerts
- `templates/input/user_input.html` - Hide honeypot field with CSS
- `core/migrations/0003_userinput_website.py` - Database migration

**Configuration:**
- `closecall/settings.py` - Changed TIME_ZONE from 'UTC' to 'America/Denver'

**Tests:**
- `tests/test_authentication.py` - Updated to use TransactionTestCase for signal-related tests

**Reporting:**
- `registration_report.py` - Added orphaned accounts section, fixed timezone display
