from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.utils import timezone

from registration.backends.default.views import RegistrationView as DefaultRegistrationView

from core.spamshield import (
    extract_client_ip,
    normalize_email,
    record_spam_hit,
    is_blocked,
)


class CloseCallRegistrationView(DefaultRegistrationView):
    """Custom registration view that silently drops honeypot submissions."""

    def _registration_success_response(self, email):
        """Mirror the default success redirect without creating a user."""
        if hasattr(self.request, "session"):
            self.request.session['registration_email'] = email

        success_url = self.get_success_url(user=None)
        try:
            to, args, kwargs = success_url
        except ValueError:
            return redirect(success_url)
        else:
            return redirect(to, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email', '')
        ip_address = extract_client_ip(self.request)
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        normalized_email = normalize_email(email)

        if is_blocked(email=normalized_email, ip_address=ip_address):
            record_spam_hit(
                email=email,
                ip_address=ip_address,
                user_agent=user_agent,
                source='registration',
                reason='preblocked',
            )
            return self._registration_success_response(email)

        if getattr(form, 'honeypot_hit', False):
            record_spam_hit(
                email=email,
                ip_address=ip_address,
                user_agent=user_agent,
                source='registration',
                reason='honeypot',
            )
            return self._registration_success_response(email)

        return super().form_valid(form)


class CloseCallLoginView(LoginView):
    template_name = 'registration/login.html'

    def _blocked_response(self):
        response = HttpResponse(
            "<h1>418 I'm a teapot</h1><p>We see what you did there.</p>",
            status=418,
        )
        response["Refresh"] = "0;url=https://www.fbi.gov/"
        return response

    def post(self, request, *args, **kwargs):
        trap_value = (request.POST.get('email_address') or '').strip()
        username = (request.POST.get('username') or '').strip()
        ip_address = extract_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        normalized = normalize_email(trap_value or username)

        if trap_value:
            record_spam_hit(
                email=trap_value,
                ip_address=ip_address,
                user_agent=user_agent,
                source='login',
                reason='login_honeypot',
                payload=username,
            )
            return self._blocked_response()

        if is_blocked(email=normalized, ip_address=ip_address):
            record_spam_hit(
                email=username,
                ip_address=ip_address,
                user_agent=user_agent,
                source='login',
                reason='login_preblocked',
            )
            return self._blocked_response()

        return super().post(request, *args, **kwargs)


def _print_password_header(action):
    """Print formatted header for password operations."""
    print("\n")
    print("*" * 50)
    print(f"********** PASSWORD {action} **********")
    print("*" * 50)
    print()


def _print_password_footer():
    """Print formatted footer for password operations."""
    print("\n\n")


class CloseCallPasswordResetView(PasswordResetView):
    """Custom password reset view with enhanced terminal logging."""

    def get(self, request, *args, **kwargs):
        ip_address = extract_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:100]

        _print_password_header("RESET REQUEST")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password reset form viewed")
        print(f"IP Address:   {ip_address}")
        print(f"User Agent:   {user_agent}")
        _print_password_footer()

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email', '')
        ip_address = extract_client_ip(self.request)
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')[:100]

        _print_password_header("RESET SUBMITTED")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password reset email requested")
        print(f"Email:        {email}")
        print(f"IP Address:   {ip_address}")
        print(f"User Agent:   {user_agent}")
        _print_password_footer()

        return super().form_valid(form)

    def form_invalid(self, form):
        ip_address = extract_client_ip(self.request)

        _print_password_header("RESET FORM INVALID")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password reset form validation failed")
        print(f"IP Address:   {ip_address}")
        print(f"Errors:       {form.errors}")
        _print_password_footer()

        return super().form_invalid(form)


class CloseCallPasswordResetConfirmView(PasswordResetConfirmView):
    """Custom password reset confirm view with enhanced terminal logging."""

    def get(self, request, *args, **kwargs):
        ip_address = extract_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')[:100]

        _print_password_header("RESET CONFIRM PAGE")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password reset confirm page viewed")
        print(f"IP Address:   {ip_address}")
        print(f"User Agent:   {user_agent}")
        print(f"UID:          {kwargs.get('uidb64', 'N/A')}")
        _print_password_footer()

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ip_address = extract_client_ip(self.request)
        user = form.user if hasattr(form, 'user') else None

        _print_password_header("RESET COMPLETE")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password successfully reset")
        print(f"User:         {user.username if user else 'Unknown'}")
        print(f"Email:        {user.email if user else 'Unknown'}")
        print(f"IP Address:   {ip_address}")
        _print_password_footer()

        return super().form_valid(form)

    def form_invalid(self, form):
        ip_address = extract_client_ip(self.request)

        _print_password_header("RESET CONFIRM FAILED")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password reset confirmation failed")
        print(f"IP Address:   {ip_address}")
        print(f"Errors:       {form.errors}")
        _print_password_footer()

        return super().form_invalid(form)


class CloseCallPasswordChangeView(PasswordChangeView):
    """Custom password change view with enhanced terminal logging."""

    def get(self, request, *args, **kwargs):
        ip_address = extract_client_ip(request)
        user = request.user

        _print_password_header("CHANGE REQUEST")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password change form viewed")
        print(f"User:         {user.username if user.is_authenticated else 'Anonymous'}")
        print(f"IP Address:   {ip_address}")
        _print_password_footer()

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        ip_address = extract_client_ip(self.request)
        user = self.request.user

        _print_password_header("CHANGE COMPLETE")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password successfully changed")
        print(f"User:         {user.username}")
        print(f"Email:        {user.email}")
        print(f"IP Address:   {ip_address}")
        _print_password_footer()

        return super().form_valid(form)

    def form_invalid(self, form):
        ip_address = extract_client_ip(self.request)
        user = self.request.user

        _print_password_header("CHANGE FAILED")
        print(f"Timestamp:    {timezone.now()}")
        print(f"Action:       Password change validation failed")
        print(f"User:         {user.username if user.is_authenticated else 'Anonymous'}")
        print(f"IP Address:   {ip_address}")
        print(f"Errors:       {form.errors}")
        _print_password_footer()

        return super().form_invalid(form)
