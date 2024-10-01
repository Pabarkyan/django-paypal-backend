from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from history.models import History
from history.api.serializers import HistorySerializer

class HistoryApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = HistorySerializer
    filter_backends = [OrderingFilter]
    queryset = History.objects.all()
    http_method_names = ['get']

    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit', None)
        queryset = queryset.filter(
            Q(origin_user=self.request.user) | Q(target_user=self.request.user)
        )
        queryset = queryset.order_by('-created_at')

        if limit is not None:
            queryset = queryset[:int(limit)]

        return queryset