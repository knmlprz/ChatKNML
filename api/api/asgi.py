import os
from django.core.asgi import get_asgi_application
<<<<<<< HEAD
from channels.routing import ProtocolTypeRouter
=======
from channels.routing import ProtocolTypeRouter, URLRouter
>>>>>>> main

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
    }
)
