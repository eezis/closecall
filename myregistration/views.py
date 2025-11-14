from django.shortcuts import redirect

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
