# Spammer Blacklist & FBI Redirect System

**Last Updated: November 12, 2025**

## Overview

The Close Call Database implements an intelligent spammer blacklist system that detects repeat spam registrations and automatically redirects offenders to the FBI Cyber Investigation page. The system normalizes email addresses to catch variations (e.g., adding/removing periods in Gmail addresses) and maintains comprehensive logs of all blocked attempts.

## Why This Approach?

Spammers often use email variations to bypass duplicate detection:
- `r.y.a.n.w.h.ite54.7.6.34@gmail.com` (Oct 17, 2025)
- `ry.a.nwh.i.t.e.54763.4.@gmail.com` (Nov 12, 2025)

Gmail ignores periods in email addresses, so both emails deliver to the same inbox: `ryanwhite547634@gmail.com`

Our solution:
1. **Normalize** emails (remove periods, lowercase)
2. **Block** all variations of known spammers
3. **Redirect** them to the FBI Cyber Investigation page
4. **Log** all attempts for tracking

## How It Works

### Registration Flow with Blacklist Check

```
User submits registration form
    ↓
Middleware intercepts POST to /accounts/register/
    ↓
Extract email from form data
    ↓
Normalize email (remove periods, lowercase)
    ↓
Check SpammerBlacklist.objects.get(normalized_email=...)
    ↓
┌─────────────────────────────────────┐
│  NOT IN BLACKLIST  │  IN BLACKLIST  │
└─────────────────────────────────────┘
         ↓                    ↓
    Continue with          Update blacklist:
    normal registration    - Increment hit_count
                          - Add email variation
                          - Add IP address
                          - Add username
                             ↓
                          Log to spammer-to-fbi.log
                             ↓
                          Log to security.log
                             ↓
                          HTTP 302 Redirect to:
                          https://www.fbi.gov/investigate/cyber
```

### Email Normalization

The `SpammerBlacklist.normalize_email()` function:

1. **Strip whitespace** and convert to **lowercase**
2. **Remove all periods** from the local part (before @)
3. **Preserve domain** exactly

**Examples:**
```python
r.y.a.n@gmail.com              → ryan@gmail.com
R.Y.A.N@gmail.com              → ryan@gmail.com
ry.a.nwh.i.t.e.54763.4.@gmail.com → ryanwhite547634@gmail.com
test.user@example.com          → testuser@example.com
TEST@EXAMPLE.COM               → test@example.com
```

**Note:** Periods are only removed from the local part (before @), not the domain.

## Database Schema

### SpammerBlacklist Model

**File:** `users/models.py`

```python
class SpammerBlacklist(models.Model):
    # Email with periods removed and lowercased for matching
    normalized_email = CharField(max_length=254, unique=True, db_index=True)

    # JSON list of email variations we've seen
    email_variations = TextField(default='[]')

    # JSON list of IP addresses associated with this spammer
    ip_addresses = TextField(default='[]')

    # JSON list of usernames they've tried
    usernames = TextField(default='[]')

    # Reason for blacklisting
    reason = CharField(max_length=255, default='spam_registration')

    # Tracking
    first_seen = DateTimeField(auto_now_add=True)
    last_seen = DateTimeField(auto_now=True)
    hit_count = IntegerField(default=1)
```

**Fields Explained:**

- **`normalized_email`** - Canonical form (no periods, lowercase) - used for matching
- **`email_variations`** - JSON array of all email forms seen (tracks evolution)
- **`ip_addresses`** - JSON array of IPs they've used (identifies patterns)
- **`usernames`** - JSON array of usernames they've tried
- **`reason`** - Why they were blacklisted (default: 'spam_registration')
- **`first_seen`** - When first blacklisted
- **`last_seen`** - When they last tried (auto-updates)
- **`hit_count`** - Number of blocked attempts

**Example Database Record:**
```json
{
  "normalized_email": "ryanwhite547634@gmail.com",
  "email_variations": [
    "r.y.a.n.w.h.ite54.7.6.34@gmail.com",
    "ry.a.nwh.i.t.e.54763.4.@gmail.com",
    "ryanwhite547634@gmail.com"
  ],
  "ip_addresses": ["173.239.254.78", "192.168.1.100"],
  "usernames": ["Matthewwaync", "MatthewW"],
  "reason": "spam_registration",
  "first_seen": "2025-11-12T15:43:04.861250Z",
  "last_seen": "2025-11-12T16:23:15.123456Z",
  "hit_count": 3
}
```

## Implementation Details

### Middleware Integration

**File:** `core/middleware.py`

The blacklist check is implemented in `AntiCSRFBypassMiddleware.process_request()`:

```python
if '/register/' in request.path and request.method == 'POST':
    email = request.POST.get('email', 'not provided')

    if email and email != 'not provided':
        from users.models import SpammerBlacklist
        normalized = SpammerBlacklist.normalize_email(email)

        try:
            spammer = SpammerBlacklist.objects.get(normalized_email=normalized)

            # Update spammer record
            spammer.hit_count += 1

            # Track email variation
            email_variations = json.loads(spammer.email_variations)
            if email not in email_variations:
                email_variations.append(email)
                spammer.email_variations = json.dumps(email_variations)

            # Track IP address
            ip_addresses = json.loads(spammer.ip_addresses)
            if client_ip not in ip_addresses:
                ip_addresses.append(client_ip)
                spammer.ip_addresses = json.dumps(ip_addresses)

            # Track username
            usernames = json.loads(spammer.usernames)
            if username not in usernames:
                usernames.append(username)
                spammer.usernames = json.dumps(usernames)

            spammer.save()

            # Log to spammer-to-fbi.log
            spammer_fbi_logger.info(
                f"REDIRECTED TO FBI: {email} | Normalized: {normalized} | "
                f"IP: {client_ip} | Username: {username} | "
                f"Total attempts: {spammer.hit_count}"
            )

            # Redirect to FBI
            return HttpResponseRedirect('https://www.fbi.gov/investigate/cyber')

        except SpammerBlacklist.DoesNotExist:
            # Not a known spammer, continue normally
            pass
```

### Logging Configuration

**File:** `closecall/settings.py`

```python
LOGGING = {
    'handlers': {
        'spammer_fbi_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'spammer-to-fbi.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 10,
            'formatter': 'detailed'
        },
    },
    'loggers': {
        'spammer.fbi': {
            'handlers': ['spammer_fbi_file'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
```

**Log Format:**
```
INFO 2025-11-12 08:46:43,378 spammer.fbi middleware process_request 74
REDIRECTED TO FBI: ry.a.nwh.i.t.e.54763.4.@gmail.com |
Normalized: ryanwhite547634@gmail.com |
IP: 173.239.254.78 |
Username: Matthewwaync |
Total attempts: 2
```

**Log Features:**
- **Rotating** - 5MB max file size
- **10 backups** - Keeps up to 50MB of history
- **Detailed format** - Timestamp, logger name, function, line number, message
- **Mountain Time** - Matches Django TIME_ZONE setting

## Management & Operations

### Adding Spammers to Blacklist

#### Method 1: Using the Script (Recommended)

**File:** `add_spammer_to_blacklist.py`

```bash
# Edit the script to add usernames
vim add_spammer_to_blacklist.py

# Add to the spammers list:
spammers = [
    'Matthewwaync',
    'AnotherSpammer',
]

# Run the script
python add_spammer_to_blacklist.py
```

**Output:**
```
============================================================
Adding Known Spammers to Blacklist
============================================================

✓ Added r.y.a.n.w.h.ite54.7.6.34@gmail.com to blacklist
  Normalized: ryanwhite547634@gmail.com
  Username: Matthewwaync
  Reason: spam_registration
  User status: Inactive (never activated)

============================================================
Summary of Blacklist:
============================================================

Normalized Email: ryanwhite547634@gmail.com
  Email Variations: ['r.y.a.n.w.h.ite54.7.6.34@gmail.com']
  Usernames: ['Matthewwaync']
  Hit Count: 1
  First Seen: 2025-11-12 15:43:04.861250+00:00
  Last Seen: 2025-11-12 15:43:04.861264+00:00
  Reason: spam_registration
```

#### Method 2: Django Shell

```bash
python manage.py shell
```

```python
from users.models import SpammerBlacklist
from django.contrib.auth.models import User
import json

# Get the spam user
user = User.objects.get(username='SpammerUsername')

# Normalize their email
normalized = SpammerBlacklist.normalize_email(user.email)

# Create blacklist entry
spammer = SpammerBlacklist.objects.create(
    normalized_email=normalized,
    email_variations=json.dumps([user.email]),
    ip_addresses=json.dumps([]),
    usernames=json.dumps([user.username]),
    reason='spam_registration',
    hit_count=1
)

print(f"Added {user.email} to blacklist")
```

#### Method 3: Django Admin

1. Navigate to `/eeadmin/`
2. Click **Spammer Blacklist**
3. Click **Add Spammer Blacklist Entry**
4. Fill in:
   - **Normalized email:** Use `SpammerBlacklist.normalize_email(email)`
   - **Email variations:** `["original@email.com"]`
   - **IP addresses:** `[]`
   - **Usernames:** `["username"]`
   - **Reason:** "spam_registration"
5. Click **Save**

### Viewing FBI Redirect Logs

#### Method 1: Pretty Viewer Script (Recommended)

```bash
python view_fbi_redirects.py
```

**Output:**
```
██████████████████████████████████████████████████████████████████████
SPAMMER FBI REDIRECT LOG
██████████████████████████████████████████████████████████████████████

Log file: /home/eezis/code/closecall/logs/spammer-to-fbi.log
Total entries: 3

======================================================================

[1] 2025-11-12 08:46:43
    Email:      ry.a.nwh.i.t.e.54763.4.@gmail.com
    Normalized: ryanwhite547634@gmail.com
    IP:         173.239.254.78
    Username:   Matthewwaync
    Attempts:   1

[2] 2025-11-12 14:23:15
    Email:      r.y.a.n.white547634@gmail.com
    Normalized: ryanwhite547634@gmail.com
    IP:         173.239.254.78
    Username:   MatthewW
    Attempts:   2

[3] 2025-11-12 18:45:22
    Email:      RYANWHITE547634@GMAIL.COM
    Normalized: ryanwhite547634@gmail.com
    IP:         192.168.1.100
    Username:   Matthewwaync
    Attempts:   3

======================================================================
Total spammer redirects to FBI: 3
======================================================================
```

#### Method 2: Raw Log File

```bash
# View entire log
cat logs/spammer-to-fbi.log

# View last 20 lines
tail -20 logs/spammer-to-fbi.log

# Watch in real-time
tail -f logs/spammer-to-fbi.log

# Search for specific email
grep "ryanwhite" logs/spammer-to-fbi.log

# Count total redirects
wc -l logs/spammer-to-fbi.log
```

### Viewing Blacklist Status

#### Database Query

```bash
python manage.py shell
```

```python
from users.models import SpammerBlacklist
import json

# Show all blacklisted entries
for spammer in SpammerBlacklist.objects.all():
    print(f"\nNormalized: {spammer.normalized_email}")
    print(f"Variations: {json.loads(spammer.email_variations)}")
    print(f"Usernames: {json.loads(spammer.usernames)}")
    print(f"IPs: {json.loads(spammer.ip_addresses)}")
    print(f"Hit Count: {spammer.hit_count}")
    print(f"Last Seen: {spammer.last_seen}")

# Find specific entry
spammer = SpammerBlacklist.objects.get(normalized_email='ryanwhite547634@gmail.com')
print(json.loads(spammer.email_variations))
```

#### Django Admin

1. Navigate to `/eeadmin/`
2. Click **Spammer Blacklist**
3. View all entries sorted by most recent

## Testing

### Test Suite

**File:** `test_spammer_blacklist.py`

```bash
python test_spammer_blacklist.py
```

**Tests:**
1. **Email Normalization** - Verifies normalize_email() works correctly
2. **Blacklist Matching** - Confirms variations are caught
3. **Non-Matching Emails** - Ensures legitimate emails aren't blocked
4. **Blacklist Summary** - Shows current blacklist state

**Expected Output:**
```
████████████████████████████████████████████████████████████
SPAMMER BLACKLIST TEST SUITE
████████████████████████████████████████████████████████████

============================================================
Testing Email Normalization
============================================================
✓ r.y.a.n@gmail.com              → ryan@gmail.com
✓ R.Y.A.N@gmail.com              → ryan@gmail.com
✓ ry.a.nwh.i.t.e.54763.4.@gmail.com → ryanwhite547634@gmail.com
✓ test.user@example.com          → testuser@example.com

============================================================
Testing Blacklist Matching
============================================================
✓ Found blacklist entry for: ryanwhite547634@gmail.com

Testing email variations that should be blocked:
✓ BLOCKED: r.y.a.n.w.h.ite54.7.6.34@gmail.com
✓ BLOCKED: ry.a.nwh.i.t.e.54763.4.@gmail.com
✓ BLOCKED: ryanwhite547634@gmail.com
✓ BLOCKED: R.Y.A.N.WHITE.547634@GMAIL.COM

============================================================
Testing Non-Matching Emails (should NOT be blocked)
============================================================
✓ ALLOWED: legitimate.user@gmail.com
✓ ALLOWED: cyclist@example.com
✓ ALLOWED: test@closecalldatabase.com

============================================================
Test Results Summary
============================================================
Email Normalization: ✓ PASSED
Blacklist Matching:  ✓ PASSED
Non-Matching Emails: ✓ PASSED

✓ ALL TESTS PASSED
```

### Test Logger

**File:** `test_fbi_logger.py`

```bash
python test_fbi_logger.py
```

Writes a test entry to `spammer-to-fbi.log` and displays the log file contents.

## Use Cases & Examples

### Scenario 1: First-Time Spammer

**Initial Registration (Oct 17, 2025):**
- Email: `r.y.a.n.w.h.ite54.7.6.34@gmail.com`
- Username: `Matthewwaync`
- Result: Account created but never activated (is_active=False)

**Admin Action:**
```bash
python add_spammer_to_blacklist.py
# Adds Matthewwaync to blacklist
```

**Blacklist Entry Created:**
```json
{
  "normalized_email": "ryanwhite547634@gmail.com",
  "email_variations": ["r.y.a.n.w.h.ite54.7.6.34@gmail.com"],
  "hit_count": 1
}
```

### Scenario 2: Spammer Tries Again

**Second Attempt (Nov 12, 2025):**
- Email: `ry.a.nwh.i.t.e.54763.4.@gmail.com` (different periods!)
- Username: `Matthewwaync`

**System Response:**
1. Middleware normalizes: `ryanwhite547634@gmail.com`
2. Finds blacklist match
3. Updates record:
   - `hit_count`: 1 → 2
   - `email_variations`: adds new variation
4. Logs to `spammer-to-fbi.log`
5. **Redirects to:** `https://www.fbi.gov/investigate/cyber`

**Log Entry:**
```
INFO 2025-11-12 14:23:15,456 spammer.fbi middleware process_request 74
REDIRECTED TO FBI: ry.a.nwh.i.t.e.54763.4.@gmail.com |
Normalized: ryanwhite547634@gmail.com |
IP: 173.239.254.78 |
Username: Matthewwaync |
Total attempts: 2
```

### Scenario 3: Persistent Spammer

**Third Attempt (Same Day):**
- Email: `RYANWHITE547634@GMAIL.COM` (no periods, all caps!)
- Username: `MatthewW` (different username)
- IP: `192.168.1.100` (different IP)

**System Response:**
1. Still normalizes to: `ryanwhite547634@gmail.com`
2. **Still blocked** - redirected to FBI
3. Updated record tracks:
   - New username: `MatthewW`
   - New IP: `192.168.1.100`
   - `hit_count`: 2 → 3

**This demonstrates the power of normalization - no matter how they vary the email, they're caught!**

## Monitoring & Analytics

### Blacklist Statistics

```bash
python manage.py shell
```

```python
from users.models import SpammerBlacklist
import json

# Total blacklisted spammers
total = SpammerBlacklist.objects.count()
print(f"Total blacklisted: {total}")

# Total blocked attempts
total_attempts = sum(s.hit_count for s in SpammerBlacklist.objects.all())
print(f"Total blocked attempts: {total_attempts}")

# Most persistent spammer
top_spammer = SpammerBlacklist.objects.order_by('-hit_count').first()
print(f"Most persistent: {top_spammer.normalized_email} ({top_spammer.hit_count} attempts)")

# Recent activity (last 7 days)
from django.utils import timezone
from datetime import timedelta
recent = timezone.now() - timedelta(days=7)
recent_attempts = SpammerBlacklist.objects.filter(last_seen__gte=recent)
print(f"Active in last 7 days: {recent_attempts.count()}")

# Show all variations for a spammer
spammer = SpammerBlacklist.objects.get(normalized_email='ryanwhite547634@gmail.com')
print(f"\nEmail variations:")
for email in json.loads(spammer.email_variations):
    print(f"  - {email}")
```

### Log Analytics

```bash
# Count total redirects
wc -l logs/spammer-to-fbi.log

# Redirects today
grep "$(date +%Y-%m-%d)" logs/spammer-to-fbi.log | wc -l

# Unique normalized emails blocked
grep "Normalized:" logs/spammer-to-fbi.log | sort -u | wc -l

# Most active IP addresses
grep "IP:" logs/spammer-to-fbi.log | sed 's/.*IP: \([^ ]*\).*/\1/' | sort | uniq -c | sort -rn

# Activity by hour
grep "$(date +%Y-%m-%d)" logs/spammer-to-fbi.log | sed 's/.*\([0-9][0-9]:[0-9][0-9]\):.*/\1/' | cut -d: -f1 | sort | uniq -c
```

## Maintenance

### Log Rotation

Logs automatically rotate when they reach 5MB. The system keeps:
- 1 active log file: `spammer-to-fbi.log`
- 10 backup files: `spammer-to-fbi.log.1` through `spammer-to-fbi.log.10`
- Total capacity: ~55MB

### Cleaning Old Entries

To remove old blacklist entries (e.g., > 1 year inactive):

```python
from users.models import SpammerBlacklist
from django.utils import timezone
from datetime import timedelta

# Find entries not seen in 365 days
cutoff = timezone.now() - timedelta(days=365)
old_entries = SpammerBlacklist.objects.filter(last_seen__lt=cutoff)

print(f"Found {old_entries.count()} old entries")

# Review before deleting
for entry in old_entries:
    print(f"{entry.normalized_email} - Last seen: {entry.last_seen}")

# Delete if appropriate
# old_entries.delete()
```

### Database Migration

The blacklist is stored in the `users_spammerblacklist` table.

**Migration file:** `users/migrations/0003_spammerblacklist_alter_userprofile_city_and_more.py`

If you need to reset the blacklist:
```bash
# WARNING: This deletes all blacklist entries!
python manage.py shell -c "from users.models import SpammerBlacklist; SpammerBlacklist.objects.all().delete()"
```

## Security Considerations

### Privacy

The system logs:
- ✓ Email addresses (needed to track variations)
- ✓ IP addresses (needed to identify patterns)
- ✓ Usernames (attempted registrations)

**Note:** These are spam/abuse records. Retain according to your security policy.

### False Positives

**Risk:** Legitimate user shares email pattern with spammer

**Example:**
- Spammer: `john.smith123@gmail.com`
- Legitimate: `johnsmith456@gmail.com`

Both normalize to different addresses, so **no conflict**.

**However**, if you blacklist `johnsmith@gmail.com`, then ALL variations are blocked:
- `john.smith@gmail.com`
- `j.o.h.n.s.m.i.t.h@gmail.com`
- `JOHNSMITH@GMAIL.COM`

**Mitigation:** Only blacklist after verifying spam (inactive accounts, multiple attempts, etc.)

### Removal from Blacklist

If a user was incorrectly blacklisted:

```bash
python manage.py shell
```

```python
from users.models import SpammerBlacklist

# Find the entry
spammer = SpammerBlacklist.objects.get(normalized_email='user@example.com')

# Review details
print(f"Email variations: {spammer.email_variations}")
print(f"Hit count: {spammer.hit_count}")
print(f"Last seen: {spammer.last_seen}")

# Delete if appropriate
spammer.delete()
```

## Files Reference

### Core Implementation
- `users/models.py` - SpammerBlacklist model with normalize_email()
- `core/middleware.py` - Blacklist checking and redirect logic
- `closecall/settings.py` - Logging configuration

### Migrations
- `users/migrations/0003_spammerblacklist_*.py` - Database schema

### Management Scripts
- `add_spammer_to_blacklist.py` - Add users to blacklist
- `test_spammer_blacklist.py` - Comprehensive test suite
- `test_fbi_logger.py` - Test logging functionality
- `view_fbi_redirects.py` - Pretty log viewer

### Log Files
- `logs/spammer-to-fbi.log` - FBI redirects (5MB, 10 backups)
- `logs/security.log` - General security events
- `logs/django.log` - General application logs

## Troubleshooting

### Spammer Not Being Blocked

**Check if they're in the blacklist:**
```python
from users.models import SpammerBlacklist
email = "problematic@email.com"
normalized = SpammerBlacklist.normalize_email(email)
exists = SpammerBlacklist.objects.filter(normalized_email=normalized).exists()
print(f"Blacklisted: {exists}")
```

**Check middleware is installed:**
```python
from django.conf import settings
print('core.middleware.AntiCSRFBypassMiddleware' in settings.MIDDLEWARE)
```

**Check logs:**
```bash
grep "problematic@email.com" logs/django.log
```

### Log File Not Created

**Check log directory exists:**
```bash
ls -la logs/
```

**Create if needed:**
```bash
mkdir -p logs
chmod 755 logs
```

**Check logger configuration:**
```python
from django.conf import settings
import logging
logger = logging.getLogger('spammer.fbi')
print(logger.handlers)
```

### Redirect Not Working

**Test middleware manually:**
```bash
# Make a test registration attempt and check nginx logs
tail -f /var/log/nginx/access.log | grep register
```

**Check Django logs:**
```bash
tail -f logs/django.log | grep -i spammer
```

## Future Enhancements

### Potential Improvements

1. **Admin Dashboard**
   - Real-time blacklist statistics
   - Visual charts of blocked attempts
   - Quick-add interface

2. **Auto-Blacklisting**
   - Automatically blacklist after X failed attempts
   - Pattern detection (similar emails, IPs)
   - Machine learning for spam detection

3. **Email Domain Blocking**
   - Block entire domains (e.g., all @suspicious-domain.com)
   - Temporary email service detection

4. **API Integration**
   - Shared blacklist across multiple sites
   - Report spammers to central database

5. **Notification System**
   - Alert on persistent spammer (>5 attempts)
   - Daily/weekly summary emails

## Conclusion

The spammer blacklist system provides:
- ✅ **Effective blocking** of repeat spam registrations
- ✅ **Email normalization** catches variations
- ✅ **Comprehensive logging** for tracking and analysis
- ✅ **FBI redirect** discourages spammers
- ✅ **Low maintenance** - automatic tracking and rotation
- ✅ **Production-ready** - tested and documented

The next time a spammer tries to register with email variations, they'll be automatically redirected to the FBI Cyber Investigation page, and their attempt will be logged for your records.

**Key Insight:** By normalizing emails, we block not just the specific spam account, but ALL variations they might try - making it significantly harder for spammers to evade detection.
