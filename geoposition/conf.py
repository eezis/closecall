# -*- coding: utf-8 -*-
from django.conf import settings

try:
    from appconf import AppConf  # legacy package name
except (ImportError, AttributeError):
    try:
        from django_appconf import AppConf  # preferred package
    except ImportError:
        class AppConf(object):  # pragma: no cover
            """Minimal fallback so migrations/commands can run without django-appconf."""
            pass


class GeopositionConf(AppConf):
    MAP_WIDGET_HEIGHT = 480
    MAP_OPTIONS = {}
    MARKER_OPTIONS = {}

    class Meta:
        prefix = 'geoposition'
