from rest_framework import serializers
from wallet.models import Wallet


class WallerSerializer(serializers.ModelSerializer):
    wallet = Wallet()

    class Meta():
        model = Wallet
        fields = ['id', 'balance']
