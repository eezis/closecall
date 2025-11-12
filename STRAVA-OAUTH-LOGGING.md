# Strava OAuth Flow - Comprehensive Logging

## Overview
Added comprehensive logging to track the entire Strava OAuth registration flow. This will help identify where users are dropping off or experiencing errors.

## Logging Points

### 1. **Initial Button Click** (`/get-strava-login`)
**Location**: `core/views.py:redirect_to_strava_login()`

**Console Output**:
```
[STRAVA OAUTH START] User clicked 'Register with Strava' button - IP: xxx.xxx.xxx.xxx
```

**Log File**: `logs/strava.log`
```
INFO: STRAVA OAUTH INITIATED - IP: xxx.xxx.xxx.xxx, User-Agent: Mozilla/5.0...
```

**What it means**: User clicked the "Register with Strava" button and was redirected to Strava's OAuth page.

---

### 2. **Callback from Strava** (`/strava-registration`)
**Location**: `core/views.py:strava_registration()`

**Console Output**:
```
[STRAVA CALLBACK] Received callback from Strava - IP: xxx.xxx.xxx.xxx, Token: abc123defg456...
```

**Log File**: `logs/strava.log`
```
INFO: STRAVA CALLBACK - IP: xxx.xxx.xxx.xxx, Has token: True
```

**What it means**: Strava redirected the user back to CCDB after authentication. If `Has token: False`, user denied access or something went wrong at Strava.

---

### 3. **Token Exchange Request**
**Location**: `core/views.py:strava_registration()` (after callback)

**Console Output**:
```
[STRAVA TOKEN EXCHANGE] Sending token exchange request to Strava - IP: xxx.xxx.xxx.xxx
```

**Log File**: `logs/strava.log`
```
INFO: STRAVA TOKEN EXCHANGE - IP: xxx.xxx.xxx.xxx, Code: abc123defg456...
```

**What it means**: CCDB is exchanging the temporary code for an access token and athlete data.

---

### 4. **Token Exchange Response**
**Location**: `core/views.py:strava_registration()` (response from Strava)

**Console Output** (Success):
```
[STRAVA TOKEN EXCHANGE RESPONSE] Status: 200 - IP: xxx.xxx.xxx.xxx
```

**Console Output** (Failure):
```
[STRAVA TOKEN EXCHANGE FAILED] Status: 400 - IP: xxx.xxx.xxx.xxx
[STRAVA TOKEN EXCHANGE FAILED] Response: {"error": "invalid_grant", "message": "Authorization code is invalid or expired"}
```

**Log File**:
```
INFO: STRAVA TOKEN EXCHANGE RESPONSE - IP: xxx.xxx.xxx.xxx, Status: 200
```
or
```
ERROR: STRAVA TOKEN EXCHANGE FAILED - Status: 400, IP: xxx.xxx.xxx.xxx, Response: {...}
```

**What it means**:
- **200**: Success - athlete data received
- **400/401**: Invalid/expired token - user may have taken too long
- **Other codes**: API errors, rate limiting, etc.

---

### 5. **New User Detection**
**Location**: `core/views.py:strava_registration()` (after getting athlete data)

**Console Output**:
```
[STRAVA NEW USER] User 'John Smith' (ID: 12345678) doesn't exist - redirecting to email collection - IP: xxx.xxx.xxx.xxx
```

**Log File**: `logs/strava.log`
```
INFO: STRAVA NEW USER - Username: John Smith, Athlete ID: 12345678, IP: xxx.xxx.xxx.xxx - Redirecting to email collection
```

**What it means**: This is a NEW user registering for the first time via Strava. They'll be redirected to provide their email.

---

### 6. **Email Collection Page Load**
**Location**: `core/views.py:strava_complete_registration()` (GET request)

**Console Output**:
```
[STRAVA EMAIL COLLECTION PAGE] User 'John Smith' (ID: 12345678) reached email collection page - IP: xxx.xxx.xxx.xxx
```

**Log File**: `logs/strava.log`
```
INFO: STRAVA EMAIL COLLECTION PAGE - Athlete: John Smith, ID: 12345678, IP: xxx.xxx.xxx.xxx
```

**What it means**: User successfully reached the email collection page.

**If session expired**:
```
[STRAVA EMAIL COLLECTION] Session expired - no strava_athlete in session - IP: xxx.xxx.xxx.xxx
```
```
WARNING: STRAVA EMAIL COLLECTION - Session expired, IP: xxx.xxx.xxx.xxx
```

---

### 7. **Email Form Submission**
**Location**: `core/views.py:strava_complete_registration()` (POST request)

**Console Output**:
```
[STRAVA EMAIL SUBMITTED] User submitted email form - IP: xxx.xxx.xxx.xxx
[STRAVA REGISTRATION ATTEMPT] John Smith (ID: 12345678) - Email: john@example.com - IP: xxx.xxx.xxx.xxx
```

**Log File**: `logs/strava.log`
```
INFO: STRAVA EMAIL SUBMITTED - Athlete: John Smith, ID: 12345678, IP: xxx.xxx.xxx.xxx
INFO: STRAVA REGISTRATION ATTEMPT - Name: John Smith, ID: 12345678, Email: john@example.com, IP: xxx.xxx.xxx.xxx
```

**What it means**: User entered their email and submitted the form. Account creation is starting.

---

## How to Monitor

### Real-time Monitoring (Console)
```bash
# Watch the Gunicorn console output for [STRAVA ...] messages
# These appear immediately in the server console
```

### Log File Analysis
```bash
# Watch the Strava log file in real-time
tail -f /home/eezis/code/closecall/logs/strava.log

# Search for recent Strava activity
grep "STRAVA" /home/eezis/code/closecall/logs/strava.log | tail -50

# Count how many users started vs completed
grep "STRAVA OAUTH INITIATED" logs/strava.log | wc -l  # Started
grep "STRAVA REGISTRATION ATTEMPT" logs/strava.log | wc -l  # Completed email collection
```

### Identify Dropoff Points
```bash
# Compare counts at each step
echo "1. OAuth Started:"
grep "STRAVA OAUTH INITIATED" logs/strava.log | wc -l

echo "2. Callback Received:"
grep "STRAVA CALLBACK" logs/strava.log | wc -l

echo "3. Token Exchange Success:"
grep "STRAVA TOKEN EXCHANGE RESPONSE.*200" logs/strava.log | wc -l

echo "4. New Users (reached email page):"
grep "STRAVA EMAIL COLLECTION PAGE" logs/strava.log | wc -l

echo "5. Email Form Submitted:"
grep "STRAVA EMAIL SUBMITTED" logs/strava.log | wc -l

echo "6. Registration Complete:"
grep "STRAVA REGISTRATION ATTEMPT" logs/strava.log | wc -l
```

## Expected Flow for New User

1. `[STRAVA OAUTH START]` - Button clicked
2. *(User authorizes at Strava's site)*
3. `[STRAVA CALLBACK]` - Callback received
4. `[STRAVA TOKEN EXCHANGE]` - Requesting athlete data
5. `[STRAVA TOKEN EXCHANGE RESPONSE] Status: 200` - Success
6. `[STRAVA NEW USER]` - User doesn't exist
7. `[STRAVA EMAIL COLLECTION PAGE]` - Email page loaded
8. `[STRAVA EMAIL SUBMITTED]` - Email submitted
9. `[STRAVA REGISTRATION ATTEMPT]` - Creating account

## Expected Flow for Returning User

1. `[STRAVA OAUTH START]` - Button clicked
2. *(User authorizes at Strava's site)*
3. `[STRAVA CALLBACK]` - Callback received
4. `[STRAVA TOKEN EXCHANGE]` - Requesting athlete data
5. `[STRAVA TOKEN EXCHANGE RESPONSE] Status: 200` - Success
6. *(Skips email collection - user already exists)*
7. `CURRENT STRAVA REGISTRANT: ...` - Existing user logged in

## Common Failure Patterns

### User Abandons at Strava Login
- See `[STRAVA OAUTH START]` but no `[STRAVA CALLBACK]`
- **Reason**: User clicked button but didn't complete Strava authorization

### Token Exchange Fails
- See `[STRAVA CALLBACK]` but `[STRAVA TOKEN EXCHANGE FAILED]`
- **Reason**: Could be expired code, Strava API issues, rate limiting

### Session Expires
- See `[STRAVA EMAIL COLLECTION] Session expired`
- **Reason**: User took too long on email page (Django session timeout)

## Additional Changes

### Profile Completion Tracking
- Strava profiles are now marked with `profile_completed=True` when created
- This helps identify which profiles came from Strava vs manual registration

### Signal Handler Fix
- Signal handler now checks for address data before attempting geocoding
- Prevents `"None None None"` geocoding attempts for empty profiles
