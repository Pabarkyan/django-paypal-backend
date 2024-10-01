from rest_framework.serializers import ModelSerializer
from history.models import History
from user.api.serializers import UserPublicSerializer


class HistorySerializer(ModelSerializer):
    origin_user = UserPublicSerializer()
    target_user = UserPublicSerializer()
    
    class Meta:
        model = History
        fields = ['id', 'type', 'origin_user', 'target_user', 'amount', 'message', 'created_at']