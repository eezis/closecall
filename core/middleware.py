from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import hashlib
import time

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
            
            # Check if this client recently did a GET to the same path
            cache_key = f"csrf_check:{client_id}:{request.path}"
            last_get = cache.get(cache_key)
            
            # If they did GET within 60 seconds and POST has no referer, block
            if last_get and not request.META.get('HTTP_REFERER'):
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