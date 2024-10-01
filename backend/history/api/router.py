from rest_framework.routers import DefaultRouter
from history.api.views import HistoryApiViewSet

router_history = DefaultRouter()

router_history.register(prefix='history', basename='history', viewset=HistoryApiViewSet)