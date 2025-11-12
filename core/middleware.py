from django.core.cache import cache
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
import hashlib
import time
import logging
import json

# Set up loggers
logger = logging.getLogger('django')
security_logger = logging.getLogger('django.security')
users_logger = logging.getLogger('users')
spammer_fbi_logger = logging.getLogger('spammer.fbi')

class AntiCSRFBypassMiddleware(MiddlewareMixin):
    """
    Middleware to detect and block CSRF bypass attempts.
    Tracks GET->POST patterns without proper referers.
    """
    
    def process_request(self, request):
        # Only check POST requests to sensitive endpoints
        sensitive_paths = [
            '/accounts/password/reset/',
            '/accounts/register/', 
            '/contact-u/'
        ]
        
        if request.method == 'POST' and request.path in sensitive_paths:
            # Get client identifier (IP + User-Agent)
            client_ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            client_id = hashlib.md5(f"{client_ip}{user_agent}".encode()).hexdigest()
            
            # Log all POST attempts to sensitive endpoints
            if '/register/' in request.path:
                email = request.POST.get('email', 'not provided')
                username = request.POST.get('username', 'not provided')
                users_logger.info(f"Registration attempt - IP: {client_ip}, Email: {email}, Username: {username}")
                logger.info(f"Registration POST from {client_ip} to {request.path}")

                # Check spammer blacklist
                if email and email != 'not provided':
                    from users.models import SpammerBlacklist
                    normalized = SpammerBlacklist.normalize_email(email)

                    try:
                        spammer = SpammerBlacklist.objects.get(normalized_email=normalized)

                        # Update spammer record
                        spammer.hit_count += 1

                        # Add new email variation if not already tracked
                        email_variations = json.loads(spammer.email_variations)
                        if email not in email_variations:
                            email_variations.append(email)
                            spammer.email_variations = json.dumps(email_variations)

                        # Add new IP if not already tracked
                        ip_addresses = json.loads(spammer.ip_addresses)
                        if client_ip not in ip_addresses:
                            ip_addresses.append(client_ip)
                            spammer.ip_addresses = json.dumps(ip_addresses)

                        # Add new username if not already tracked
                        usernames = json.loads(spammer.usernames)
                        if username not in usernames and username != 'not provided':
                            usernames.append(username)
                            spammer.usernames = json.dumps(usernames)

                        spammer.save()

                        # Log to dedicated spammer-to-fbi.log
                        spammer_fbi_logger.info(
                            f"REDIRECTED TO FBI: {email} | Normalized: {normalized} | "
                            f"IP: {client_ip} | Username: {username} | "
                            f"Total attempts: {spammer.hit_count}"
                        )

                        # Also log to security log
                        security_logger.warning(
                            f"BLACKLISTED SPAMMER BLOCKED: {email} (normalized: {normalized}) "
                            f"- IP: {client_ip}, Username: {username}, "
                            f"Total attempts: {spammer.hit_count}"
                        )

                        # Redirect spammer to FBI Cyber Investigation page
                        return HttpResponseRedirect('https://www.fbi.gov/investigate/cyber')

                    except SpammerBlacklist.DoesNotExist:
                        # Not a known spammer, continue normally
                        pass
            elif '/login/' in request.path:
                username = request.POST.get('username', 'not provided')
                users_logger.info(f"Login attempt - IP: {client_ip}, Username: {username}")

            # Check if this client recently did a GET to the same path
            cache_key = f"csrf_check:{client_id}:{request.path}"
            last_get = cache.get(cache_key)

            # If they did GET within 60 seconds and POST has no referer, block
            if last_get and not request.META.get('HTTP_REFERER'):
                security_logger.warning(f"Potential CSRF bypass attempt from {client_ip} on {request.path}")
                # Increment abuse counter
                abuse_key = f"csrf_abuse:{client_id}"
                abuse_count = cache.get(abuse_key, 0) + 1
                cache.set(abuse_key, abuse_count, 3600)  # Remember for 1 hour
                
                if abuse_count >= 3:
                    # Block this client completely for 24 hours
                    block_key = f"blocked:{client_id}"
                    cache.set(block_key, True, 86400)
                    return HttpResponseForbidden("Access denied due to suspicious activity")
                    
        elif request.method == 'GET' and request.path in sensitive_paths:
            # Track GET requests to sensitive paths
            client_ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            client_id = hashlib.md5(f"{client_ip}{user_agent}".encode()).hexdigest()
            
            cache_key = f"csrf_check:{client_id}:{request.path}"
            cache.set(cache_key, time.time(), 60)  # Remember for 60 seconds
            
        # Check if client is blocked
        client_ip = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        client_id = hashlib.md5(f"{client_ip}{user_agent}".encode()).hexdigest()
        
        if cache.get(f"blocked:{client_id}"):
            return HttpResponseForbidden("Access denied")
            
        return None
    
    def get_client_ip(self, request):
        """Get the real client IP, considering proxies."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_exception(self, request, exception):
        """Log exceptions on sensitive endpoints"""
        sensitive_paths = [
            '/accounts/password/reset/',
            '/accounts/register/',
            '/contact-u/'
        ]

        if request.path in sensitive_paths:
            client_ip = self.get_client_ip(request)
            users_logger.error(f"Error on {request.path} from {client_ip}: {str(exception)}")

            # For registration errors, try to capture the attempted email
            if '/register/' in request.path and request.method == 'POST':
                email = request.POST.get('email', 'not captured')
                username = request.POST.get('username', 'not captured')
                users_logger.error(f"Registration failed - Email: {email}, Username: {username}, Error: {type(exception).__name__}: {str(exception)[:200]}")
                security_logger.error(f"Registration error from {client_ip}: {type(exception).__name__}")

        return None