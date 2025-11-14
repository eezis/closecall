from __future__ import annotations

from typing import Optional

from django.db.models import Q

from django.apps import apps


GMAIL_DOMAINS = {"gmail.com", "googlemail.com"}


def normalize_email(email: Optional[str]) -> str:
    """Normalize email addresses for consistent spam comparison."""
    if not email:
        return ""

    email = email.strip().lower()
    if "@" not in email:
        return email

    local, domain = email.split("@", 1)
    domain = domain.lower()

    if domain in GMAIL_DOMAINS:
        # Gmail ignores dots and anything after a plus in the local part.
        local = local.split("+", 1)[0].replace(".", "")
        domain = "gmail.com"

    return f"{local}@{domain}"


def extract_client_ip(request) -> str:
    """Return the best-guess client IP from the request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "") or ""


def _truncate_payload(payload: Optional[str], limit: int = 500) -> str:
    if not payload:
        return ""
    payload = payload.strip()
    if len(payload) <= limit:
        return payload
    return f"{payload[:limit]}…"


def record_spam_hit(
    *,
    email: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    source: str = "other",
    reason: str = "",
    payload: Optional[str] = None,
) -> SpamTrapEntry:
    """Persist spam intelligence for future blocking."""
    normalized = normalize_email(email)
    SpamTrap = apps.get_model('core', 'SpamTrapEntry')
    entry = SpamTrap.objects.create(
        email_normalized=normalized,
        email_raw=email or "",
        ip_address=ip_address,
        user_agent=(user_agent or "")[:512],
        source=source,
        reason=reason,
        payload_excerpt=_truncate_payload(payload),
    )
    return entry


def is_blocked(*, email: Optional[str] = None, ip_address: Optional[str] = None) -> bool:
    """Check whether the email or IP previously tripped our spam traps."""
    query = Q()
    normalized = normalize_email(email)
    if normalized:
        query |= Q(email_normalized=normalized)
    if ip_address:
        query |= Q(ip_address=ip_address)

    if not query:
        return False

    SpamTrap = apps.get_model('core', 'SpamTrapEntry')
    return SpamTrap.objects.filter(query).exists()
