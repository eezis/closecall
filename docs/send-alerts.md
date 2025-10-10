# Incident Email Notification Process

## Overview
When a serious incident is reported, you can send email notifications to all registered users in the area who have opted in to receive incident alerts.

## Email Configuration
- **Service**: Resend (configured in `.env`)
- **Sender**: `noreply@alert.closecalldatabase.com` (verified domain)
- **Recipients**: Users within configurable radius (default 60 miles) who have `email_incidents=True`

## Step-by-Step Process

### 1. Review Incident in Admin
```
https://closecalldatabase.com/eeadmin/incident/incident/
```
- Find the incident by ID or search
- Review the report for:
  - Accuracy of information
  - Vehicle description
  - License plate information
  - Severity (threat level)
- Mark as `reviewed=True` if appropriate

### 2. Check Email Status
In the admin, look for:
- **email_sent**: Should be `False` (if already `True`, emails were already sent)
- **email_sent_on**: Date/time when emails were sent (if previously sent)
- **email_text**: Copy of the email that was sent (if previously sent)

### 3. Send Email Notifications

#### Setting the Radius

**Default radius**: 60 miles

You can customize the search radius based on incident severity:

- **20-30 miles**: Local incidents, specific intersections, neighborhood issues
- **40-50 miles**: City-wide or county incidents
- **60 miles** (default): Serious incidents, hit-and-run drivers
- **80-100 miles**: Regional threats, dangerous drivers spotted across multiple areas

Add `--radius MILES` to any command to set the search radius.

#### Option A: Test Mode (Recommended First)
See who would receive emails without actually sending:

```bash
cd ~/code/closecall
source .venv/bin/activate
python utils/send_incident_emails.py INCIDENT_ID --test
```

Examples:
```bash
# Default 60 mile radius
python utils/send_incident_emails.py 1234 --test

# 30 mile radius
python utils/send_incident_emails.py 1234 --radius 30 --test

# 20 mile radius
python utils/send_incident_emails.py 1234 --radius 20 --test
```

#### Option B: Send Test Email to Yourself
Send one test email to verify everything works:

```bash
# Default radius
python utils/send_incident_emails.py 1234 --test-email ernest.ezis@gmail.com

# With custom radius
python utils/send_incident_emails.py 1234 --radius 30 --test-email ernest.ezis@gmail.com
```

#### Option C: Send to All Users (Production)
After testing, send to all users in the area:

```bash
# Default 60 mile radius
python utils/send_incident_emails.py 1234

# Custom 30 mile radius
python utils/send_incident_emails.py 1234 --radius 30

# Custom 20 mile radius
python utils/send_incident_emails.py 1234 --radius 20
```

### 4. Verify Email Was Sent
- Script will update the incident automatically:
  - `email_sent` → `True`
  - `email_sent_on` → Current timestamp
  - `email_text` → Copy of message sent
- Check admin to confirm fields were updated

## Email Template

Users receive an HTML email with:
- Subject: "Close Call Database - Incident Reported in your Area"
- Link to incident details
- Request to report if they've encountered the vehicle
- Social media links
- Sender: noreply@alert.closecalldatabase.com

## Troubleshooting

### Email Doesn't Send
1. Check Resend API key in `.env`:
   ```bash
   grep EMAIL /home/eezis/code/closecall/.env
   ```
2. Verify domain is verified in Resend dashboard
3. Check Django logs: `tail -f /home/eezis/code/closecall/django.log`

### No Users Found
- Verify incident has valid latitude/longitude coordinates
- Check that users exist with `email_incidents=True`:
  ```python
  from users.models import UserProfile
  UserProfile.objects.filter(email_incidents=True).count()
  ```
- Try larger radius (e.g., `--radius 100`)

### Users Not Getting Positioned Correctly
User positions are geocoded from their city/state/zip. If having issues:
1. Check user profile has location data
2. Run geocoding manually in admin
3. Check `position` field format: `(latitude, longitude)`

## Safety Features

✅ **Test mode** - Preview recipients without sending
✅ **Confirmation required** - Must type "yes" to send in production
✅ **Duplicate check** - Warns if incident already has emails sent
✅ **Email tracking** - Records when/what was sent
✅ **Error handling** - Shows which emails fail and why

## Quick Reference

| Command | Purpose |
|---------|---------|
| `--test` | Show who would get emails (don't send) |
| `--test-email EMAIL` | Send one test email |
| `--radius MILES` | Change search radius (default: 60) |
| No flags | Send to all users (production) |

## Example Workflow

```bash
# Step 1: Activate environment
cd ~/code/closecall
source .venv/bin/activate

# Step 2: Test mode - see who would get emails
python utils/send_incident_emails.py 1467 --test

# Step 3: Send test to yourself
python utils/send_incident_emails.py 1467 --test-email ernest.ezis@gmail.com

# Step 4: Check your email - looks good?
# Step 5: Send for real
python utils/send_incident_emails.py 1467

# Type "yes" to confirm
```

## Notes

- **Old Script**: `utils/email-incident-report.py` is deprecated (requires manual editing)
- **New Script**: `utils/send_incident_emails.py` is command-line based (no editing needed)
- Both scripts use the same email functions and Resend configuration
- Emails are sent from `noreply@alert.closecalldatabase.com` (verified Resend domain)
