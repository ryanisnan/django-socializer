from django.dispatch.dispatcher import Signal


socializer_auto_takedown = Signal(providing_args=['content_object'])
