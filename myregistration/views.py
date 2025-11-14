from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

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
        trap_value = (request.POST.get('trap_email') or '').strip()
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
