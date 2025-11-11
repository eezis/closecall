---
description: Run comprehensive health check of CCDB production system
---

# CCDB Health Check

Run a comprehensive health check of the Close Call Database production system.

## Instructions

Execute the CCDB health check script and analyze the results:

```bash
python .claude/commands/ccdb-health-check.py
```

## Analysis Required

After running the script, provide:

1. **Status Summary**: Overall system health (HEALTHY, OPERATIONAL WITH WARNINGS, or DEGRADED)
2. **Critical Issues**: Any services that are down or misconfigured
3. **Architecture Verification**: Confirm the proper chain (Cloudflare → Nginx → Gunicorn)
4. **Log Issues**: Highlight any errors or warnings found in logs
5. **Recommendations**: Suggest fixes for any problems found

## What This Checks

- Cloudflare tunnel configuration and routing
- Nginx status (port 8888)
- Gunicorn status (port 8890)
- Static files availability
- Service chain connectivity
- Django application logs
- Nginx error logs
- Recent activity and sessions

Remember: This is a LIVE PRODUCTION SITE. Do not restart or modify any services unless explicitly approved by the user.
