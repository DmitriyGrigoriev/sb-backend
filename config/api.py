from rest_framework import routers
#from apps.users.views import UserViewSet
#from apps.transportconf.views import TerminalViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'

# Users API
#api.register(r'users', UserViewSet)
#api.register('transport/terminal', TerminalViewSet)
