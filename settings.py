try:
    from django.conf.settings import SOCIALIZER_AUTO_TAKEDOWN
except ImportError:
    SOCIALIZER_AUTO_TAKEDOWN = False

try:
    from django.conf.settings import SOCIALIZER_AUTO_TAKEDOWN_TRIGGER
except ImportError:
    SOCIALIZER_AUTO_TAKEDOWN_TRIGGER = 5