#!/usr/bin/env python3
"""
Close Call Database Health Check
Slash command for Claude Code to check the health of the CCDB services
"""

import subprocess
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
import json
import sys

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def run_command(cmd):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode
    except Exception as e:
        return str(e), 1

def check_port(port):
    """Check if a service is listening on a port"""
    # Try multiple methods to check port
    # Method 1: lsof (might need permissions)
    output, code = run_command(f"lsof -i:{port} 2>/dev/null | grep LISTEN")
    if output:
        return True

    # Method 2: ss command (more reliable)
    output, code = run_command(f"ss -tlpn 2>/dev/null | grep ':{port}'")
    if output:
        return True

    # Method 3: netstat
    output, code = run_command(f"netstat -tlpn 2>/dev/null | grep ':{port}'")
    if output:
        return True

    # Method 4: Try to connect
    output, code = run_command(f"timeout 1 bash -c 'echo > /dev/tcp/localhost/{port}' 2>/dev/null")
    return code == 0

def check_process(process_name):
    """Check if a process is running"""
    output, code = run_command(f"ps aux | grep -v grep | grep '{process_name}'")
    return bool(output)

def get_cloudflare_config():
    """Read and parse Cloudflare config"""
    config_path = Path.home() / '.cloudflared' / 'config.yml'
    if not config_path.exists():
        return None

    with open(config_path, 'r') as f:
        lines = f.readlines()

    # Extract Close Call Database routes
    ccdb_config = {}
    for i, line in enumerate(lines):
        # Look for hostname line (not comments)
        if 'hostname:' in line and 'closecalldatabase.com' in line:
            # Look for the service line after hostname
            for j in range(i+1, min(i+3, len(lines))):
                if 'service:' in lines[j]:
                    match = re.search(r'service:\s*http://localhost:(\d+)', lines[j])
                    if match:
                        ccdb_config['port'] = match.group(1)
                        break
            break  # Found first closecalldatabase.com entry

    return ccdb_config

def check_static_files():
    """Check if static files exist"""
    static_dir = Path('/home/eezis/code/closecall/nginx-root/static')
    if not static_dir.exists():
        return False, "Static directory not found"

    # Check for key directories
    required_dirs = ['css', 'js', 'images', 'admin']
    missing = []
    for dir_name in required_dirs:
        if not (static_dir / dir_name).exists():
            missing.append(dir_name)

    if missing:
        return False, f"Missing directories: {', '.join(missing)}"

    # Count files
    file_count = sum(1 for _ in static_dir.rglob('*') if _.is_file())
    return True, f"{file_count} files"

def analyze_django_logs():
    """Analyze Django application logs"""
    log_dir = Path('/home/eezis/code/closecall/logs')
    issues = []
    warnings = []

    if not log_dir.exists():
        return ["Log directory not found"], []

    # Check main django.log
    django_log = log_dir / 'django.log'
    if django_log.exists():
        with open(django_log, 'r') as f:
            lines = f.readlines()

        # Count recent errors (last 24 hours)
        now = datetime.now()
        error_count = 0
        warning_count = 0
        not_found_resources = set()

        for line in lines[-1000:]:  # Check last 1000 lines
            if 'ERROR' in line:
                error_count += 1
                if error_count <= 3:  # Show first 3 errors
                    issues.append(f"ERROR: {line.strip()[:100]}...")
            elif 'WARNING' in line:
                warning_count += 1
                # Extract 404s
                if 'Not Found:' in line:
                    match = re.search(r'Not Found: (.+?)$', line)
                    if match:
                        not_found_resources.add(match.group(1))

        if error_count > 0:
            issues.append(f"Found {error_count} ERROR entries in recent logs")
        if warning_count > 0:
            warnings.append(f"Found {warning_count} WARNING entries")
        if not_found_resources:
            warnings.append(f"404 Not Found for: {', '.join(list(not_found_resources)[:5])}")

    # Check other log files
    for log_file in ['errors.log', 'security.log', 'strava.log']:
        path = log_dir / log_file
        if path.exists() and path.stat().st_size > 0:
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > 10:
                warnings.append(f"{log_file} is {size_mb:.1f}MB (consider rotation)")

    return issues, warnings

def analyze_nginx_logs():
    """Check nginx error logs"""
    issues = []

    # Check nginx error log
    nginx_error = Path('/var/log/nginx/closecall.error.log')
    if nginx_error.exists() and nginx_error.stat().st_size > 0:
        with open(nginx_error, 'r') as f:
            lines = f.readlines()[-100:]  # Last 100 lines

        for line in lines:
            if 'emerg' in line or 'alert' in line:
                issues.append(f"NGINX Critical: {line.strip()[:100]}")
            elif 'error' in line:
                issues.append(f"NGINX Error: {line.strip()[:100]}")

    return issues

def main():
    print(f"\n{BOLD}{BLUE}═══════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}{BLUE}     Close Call Database Health Check{RESET}")
    print(f"{BOLD}{BLUE}═══════════════════════════════════════════════════════{RESET}\n")

    # Read configurations
    cf_config = get_cloudflare_config()

    # Expected ports
    nginx_port = 8888
    gunicorn_port = 8890
    expected_cf_port = nginx_port  # Should route to nginx

    # Check Cloudflare configuration
    cf_ok = False
    if cf_config and cf_config.get('port') == str(expected_cf_port):
        cf_ok = True
        print(f"  {GREEN}✅{RESET} Cloudflare configured correctly (routes to port {expected_cf_port})")
    elif cf_config and cf_config.get('port') == str(gunicorn_port):
        print(f"  {YELLOW}⚠️{RESET}  Cloudflare bypassing nginx (routes directly to gunicorn:{gunicorn_port})")
    else:
        print(f"  {RED}❌{RESET} Cloudflare configuration issue")

    # Check nginx
    nginx_ok = check_port(nginx_port)
    if nginx_ok:
        print(f"  {GREEN}✅{RESET} Nginx is running and listening on port {nginx_port}")
    else:
        print(f"  {RED}❌{RESET} Nginx is NOT listening on port {nginx_port}")

    # Check gunicorn
    gunicorn_ok = check_port(gunicorn_port)
    if gunicorn_ok:
        print(f"  {GREEN}✅{RESET} Gunicorn is running and listening on port {gunicorn_port}")
    else:
        print(f"  {RED}❌{RESET} Gunicorn is NOT listening on port {gunicorn_port}")

    # Check static files
    static_ok, static_msg = check_static_files()
    if static_ok:
        print(f"  {GREEN}✅{RESET} Static files exist in nginx-root/static/ ({static_msg})")
    else:
        print(f"  {RED}❌{RESET} Static files issue: {static_msg}")

    # Check architecture
    if cf_ok and nginx_ok and gunicorn_ok:
        print(f"  {GREEN}✅{RESET} Proper architecture: Cloudflare → Nginx ({nginx_port}) → Gunicorn ({gunicorn_port})")
    else:
        print(f"  {YELLOW}⚠️{RESET}  Architecture incomplete or misconfigured")

    # Check if cloudflared is running
    cf_running = check_process('cloudflared')
    if cf_running:
        print(f"  {GREEN}✅{RESET} Cloudflare tunnel daemon is running")
    else:
        print(f"  {RED}❌{RESET} Cloudflare tunnel daemon is NOT running")

    # Test the chain
    print(f"\n{BOLD}Testing Service Chain:{RESET}")

    # Test nginx to gunicorn
    response, code = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:{nginx_port}")
    if response == '200':
        print(f"  {GREEN}✅{RESET} Nginx → Gunicorn proxy working (HTTP 200)")
    else:
        print(f"  {RED}❌{RESET} Nginx → Gunicorn proxy issue (HTTP {response})")

    # Log analysis
    print(f"\n{BOLD}Now checking the logs for errors and issues...{RESET}\n")

    django_issues, django_warnings = analyze_django_logs()
    nginx_issues = analyze_nginx_logs()

    # Display log analysis
    if django_issues or nginx_issues:
        print(f"{BOLD}{RED}Issues Found:{RESET}")
        for issue in django_issues:
            print(f"  • {issue}")
        for issue in nginx_issues:
            print(f"  • {issue}")
        print()

    if django_warnings:
        print(f"{BOLD}{YELLOW}Warnings:{RESET}")
        for warning in django_warnings:
            print(f"  • {warning}")
        print()

    if not django_issues and not nginx_issues and not django_warnings:
        print(f"  {GREEN}✅{RESET} No significant issues found in logs")

    # Recent activity
    print(f"\n{BOLD}Recent Activity:{RESET}")

    # Check last request time
    access_log = Path('/var/log/nginx/closecall.access.log')
    if access_log.exists() and access_log.stat().st_size > 0:
        last_modified = datetime.fromtimestamp(access_log.stat().st_mtime)
        time_diff = datetime.now() - last_modified
        if time_diff < timedelta(minutes=5):
            print(f"  • Last nginx request: {time_diff.seconds} seconds ago")
        else:
            print(f"  • Last nginx request: {time_diff} ago")

    # Check Django sessions
    session_count, _ = run_command("ls /home/eezis/code/closecall/sessions 2>/dev/null | wc -l")
    if session_count:
        print(f"  • Active session files: {session_count}")

    # Summary
    print(f"\n{BOLD}{BLUE}═══════════════════════════════════════════════════════{RESET}")

    all_ok = cf_ok and nginx_ok and gunicorn_ok and static_ok and not django_issues and not nginx_issues
    if all_ok:
        print(f"{BOLD}{GREEN}✨ System Status: HEALTHY ✨{RESET}")
    elif nginx_ok and gunicorn_ok:
        print(f"{BOLD}{YELLOW}⚠️  System Status: OPERATIONAL WITH WARNINGS ⚠️{RESET}")
    else:
        print(f"{BOLD}{RED}🔥 System Status: DEGRADED - ATTENTION REQUIRED 🔥{RESET}")

    print(f"{BOLD}{BLUE}═══════════════════════════════════════════════════════{RESET}\n")

if __name__ == "__main__":
    main()