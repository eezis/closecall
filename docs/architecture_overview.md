# Architecture Overview - Close Call Database

**Last Updated: November 11, 2025**

## Network Architecture

The Close Call Database uses a multi-layered architecture for security, performance, and reliability:

```
Internet
    ↓
Cloudflare Tunnel (cloudflared)
    ↓
Nginx (port 8888)
    ↓
Gunicorn (port 8890)
    ↓
Django Application
```

## Component Details

### 1. Cloudflare Tunnel
- **Tunnel ID**: b165ac0a-28c3-45e5-85cc-38fc0e32db7a (named "scrumble")
- **Configuration**: `~/.cloudflared/config.yml`
- **Routes**:
  - `closecalldatabase.com` → `http://localhost:8888`
  - `www.closecalldatabase.com` → `http://localhost:8888`
  - `test.closecalldatabase.com` → `http://localhost:8888`

**Benefits**:
- DDoS protection
- SSL/TLS termination
- Global CDN
- Hides server IP address
- No exposed ports to internet

### 2. Nginx
- **Port**: 8888
- **Configuration**: `/home/eezis/code/closecall/nginx/sites-available/closecall`
- **Upstream**: Proxies to Gunicorn at `127.0.0.1:8890`
- **Features**:
  - Static file serving from `nginx-root/static/`
  - Request buffering
  - Caching headers
  - Gzip compression
  - Connection pooling (keepalive 32)

**Nginx Upstream Configuration**:
```nginx
upstream closecall_gunicorn {
    server 127.0.0.1:8890 fail_timeout=0;
    keepalive 32;
}
```

### 3. Gunicorn
- **Port**: 8890
- **Configuration**: `gunicorn-local.conf.py` (development) / `gunicorn.conf.py` (production)
- **Workers**: 2 (local) / CPU cores * 2 + 1 (production)
- **Features**:
  - WSGI server for Python
  - Worker process management
  - Automatic worker restart after 1000 requests
  - Request timeout: 30 seconds

**Gunicorn Binding**:
```python
bind = "127.0.0.1:8890"  # CRITICAL: Must be 8890, not 8888
```

### 4. Django Application
- **Version**: Django 5.1.3
- **Database**: PostgreSQL with PostGIS
- **Static Files**: Collected to `nginx-root/static/`
- **Media Files**: Stored in `media/`
- **Sessions**: 15-month duration

## Multi-Service Environment

The Close Call Database runs alongside other services, managed by `~/start_all_servers_with_prefixes.sh`:

| Service | Port | Prefix | Description |
|---------|------|--------|-------------|
| RoadWise MVP | 9988 | [FP] | FastAPI application |
| Game Server | 7373 | [GM] | Scrumble game |
| **Close Call Nginx** | **8888** | **[CC]** | **Reverse proxy** |
| **Close Call Gunicorn** | **8890** | **[CC]** | **WSGI server** |
| K360 POC | 7788 | [K3] | Django development |
| Caddy | 7777 | - | Systemd service |
| Cloudflare Tunnel | - | [CF] | All services |

## Data Flow

### Request Path
1. **User** makes request to `closecalldatabase.com`
2. **Cloudflare** handles DNS, SSL, DDoS protection
3. **Cloudflare Tunnel** forwards to localhost:8888
4. **Nginx** receives request on port 8888
   - Serves static files directly
   - Proxies dynamic requests to Gunicorn
5. **Gunicorn** on port 8890 runs Django application
6. **Django** processes request, queries PostgreSQL
7. Response flows back through the chain

### Static Files
```
User → Cloudflare → Nginx (serves directly from nginx-root/static/)
```

### Dynamic Content
```
User → Cloudflare → Nginx → Gunicorn → Django → PostgreSQL
```

## Security Layers

1. **Cloudflare**: First line of defense
   - DDoS mitigation
   - Bot protection
   - SSL/TLS encryption
   - IP reputation filtering

2. **Nginx**: Application firewall
   - Rate limiting capabilities
   - Request size limits
   - Header filtering

3. **Django**: Application security
   - CSRF protection
   - Session management
   - User authentication
   - Custom middleware for security logging

## Configuration Files

### Critical Files
- `~/.cloudflared/config.yml` - Cloudflare tunnel routes
- `/home/eezis/code/closecall/nginx/sites-available/closecall` - Nginx configuration
- `/home/eezis/code/closecall/gunicorn-local.conf.py` - Local Gunicorn config
- `/home/eezis/code/closecall/gunicorn.conf.py` - Production Gunicorn config
- `/home/eezis/code/closecall/closecall/settings.py` - Django settings
- `~/start_all_servers_with_prefixes.sh` - Service startup script

### Port Configuration
**CRITICAL**: The port assignments are fixed and must not be changed:
- Nginx MUST listen on port 8888
- Gunicorn MUST bind to port 8890
- Changing these will break the site

## Logging Architecture

Logs flow through multiple systems:
- **Cloudflare**: Access logs in dashboard
- **Nginx**: Access logs (currently to stdout with [CC] prefix)
- **Gunicorn**: Application logs (stdout/stderr)
- **Django**: Application logs to `logs/` directory

See `logging_overview.md` for detailed logging configuration.

## Development vs Production

### Development (Local)
- Uses `gunicorn-local.conf.py`
- Logs to console with [CC] prefix
- Debug mode enabled
- 2 workers

### Production
- Uses `gunicorn.conf.py`
- Logs to `/var/log/gunicorn/`
- Debug mode disabled
- Workers = CPU cores * 2 + 1
- Runs as www-data user

## Troubleshooting

### Site is Down
1. Check port configuration:
   - Gunicorn MUST be on 8890
   - Nginx MUST be on 8888
2. Verify services are running:
   ```bash
   lsof -ti:8888  # Should show nginx
   lsof -ti:8890  # Should show gunicorn
   ```

### 502 Bad Gateway
- Usually means Gunicorn is not running or on wrong port
- Check `gunicorn-local.conf.py` has `bind = "127.0.0.1:8890"`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Verify nginx serves from `nginx-root/static/`

## Startup and Shutdown

### Start All Services
```bash
~/start_all_servers_with_prefixes.sh
```

### Stop All Services
```bash
~/stop_all_servers.sh
```

### Restart Close Call Only
```bash
# DO NOT restart without permission in production
./restart_ccdb.sh
```

## Important Notes

1. **Never change port 8890 in Gunicorn config** - This will break the nginx proxy
2. **Never change port 8888 in Nginx config** - This will break Cloudflare tunnel
3. **Always use the startup script** - It ensures proper logging prefixes
4. **Monitor logs** - Check both console output and `logs/` directory
5. **Coordinate changes** - Multiple Claude sessions may conflict