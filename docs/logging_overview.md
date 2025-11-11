# Logging Overview - Close Call Database

**Last Updated: November 11, 2025**

## Architecture

The Close Call Database uses a dual logging approach to ensure comprehensive monitoring during both development and production environments.

## Console Output

Console logging provides real-time feedback with service prefixes when running multiple services:

- All console output gets the `[CC]` prefix via `start_all_servers_with_prefixes.sh`
- The prefix is added by `sed 's/^/[CC] /'` in the startup script
- Shows HTTP access logs from gunicorn
- Shows Django application logs in real-time

### Service Prefixes

When running multiple services via `start_all_servers_with_prefixes.sh`:
- `[CC]` = CloseCallDatabase.com (ports 8888/8890)
- `[FP]` = FlectionPoint/Roadwise (port 9988)
- `[GM]` = Games.amlit.com (port 7373)
- `[K3]` = K360-POC.milehighsandbox.com (port 7788)
- `[CF]` = Cloudflare Tunnel

## Log Files

All application logs are written to the `logs/` directory with automatic rotation to prevent disk space issues:

### Log File Structure

| File | Purpose | Max Size | Backups | Log Level |
|------|---------|----------|---------|-----------|
| `django.log` | General Django application logs | 10MB | 5 | INFO/DEBUG |
| `strava.log` | Strava OAuth and registration events | 5MB | 3 | DEBUG |
| `users.log` | User registration attempts with emails | 5MB | 3 | DEBUG |
| `security.log` | Security events and CSRF attempts | 10MB | 10 | WARNING |
| `errors.log` | All ERROR level messages | 10MB | 10 | ERROR |
| `incidents.log` | Incident reporting events | 10MB | 5 | DEBUG |

### Log Rotation

- Each log file has size limits (5-10MB depending on importance)
- Automatic rotation with backup counts (3-10 files)
- Prevents disk space issues in production

## Configuration

### Development Environment

- **Gunicorn**: Configured in `gunicorn-local.conf.py`
  - Access logs to stdout with format: `[CC] %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s`
  - Error logs to stdout
  - Both streams get `[CC]` prefix from startup script

- **Django Logging**: Configured in `closecall/settings.py`
  - DEBUG level for Django logger in development
  - All loggers write to both console and files
  - Request/response logging enabled

### Production Environment

- **Gunicorn**: Configured in `gunicorn.conf.py`
  - Access logs to `/var/log/gunicorn/ccdb-access.log`
  - Error logs to `/var/log/gunicorn/ccdb-error.log`
  - Runs as `www-data` user/group

## Middleware Logging

### AntiCSRFBypassMiddleware

Logs the following security events:
- Registration attempts with IP, email, and username
- Login attempts with IP and username
- Potential CSRF bypass attempts
- Blocks repeated CSRF bypass attempts (3+ attempts)

### Registration Tracking

All registration attempts are logged with:
- IP address
- Email address (when provided)
- Username
- User agent
- Error details for failed attempts

## Usage Examples

### Viewing Logs

```bash
# Real-time console logs (all services)
./start_all_servers_with_prefixes.sh

# View specific log files
tail -f logs/django.log
tail -f logs/users.log
tail -f logs/security.log

# Check for registration attempts
grep "Registration attempt" logs/users.log

# Monitor security events
tail -f logs/security.log
```

### Testing Logging

A test script is available at `test_logging.py`:
```bash
python test_logging.py
```

This will write test messages to all configured loggers and report file sizes.

## Troubleshooting

### Empty Log Files

If log files appear empty:
1. The application may be running with gunicorn in console-only mode
2. Django's internal logging only writes when code explicitly calls loggers
3. Most activity is HTTP access logs (shown in console) not application events

### Missing Email in Registration Logs

The middleware captures POST data, but if registration fails before form validation, email may show as "not provided" or "not captured".

## Implementation Notes

- Logging configuration is in `closecall/settings.py` (lines 181-294)
- Middleware logging is in `core/middleware.py`
- The `LOG_DIR` is automatically created if missing
- Old logs in project root have been removed (previously 2.2MB `django.log`)