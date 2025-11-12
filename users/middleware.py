"""
Middleware to ensure users complete their profile before accessing the site.
"""
from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """
    Redirect logged-in users with incomplete profiles to the profile creation page.

    This prevents users from bypassing profile completion by navigating away from
    the activation page or opening the site in a different tab.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check logged-in users
        if request.user.is_authenticated:
            # Allow access to these paths without profile
            allowed_paths = [
                reverse('create-user-profile'),
                reverse('auth_logout'),
                '/static/',
                '/media/',
                '/admin/',  # Allow staff to access admin
            ]

            # Check if current path is allowed
            is_allowed_path = any(
                request.path.startswith(path)
                for path in allowed_paths
            )

            if not is_allowed_path:
                # Check if user has incomplete profile
                try:
                    profile = request.user.profile

                    # Check if profile is complete (has required location data)
                    city_missing = not profile.city or profile.city.strip() == ''
                    state_missing = not profile.state or profile.state.strip() == ''
                    country_missing = not profile.country or profile.country.strip() == ''

                    if city_missing or state_missing or country_missing:
                        # Profile incomplete, redirect to profile creation
                        return redirect('create-user-profile')

                except Exception:
                    # No profile exists (shouldn't happen with signal handler, but be safe)
                    return redirect('create-user-profile')

        response = self.get_response(request)
        return response
