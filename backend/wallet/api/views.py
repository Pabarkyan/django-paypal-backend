import stripe
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from wallet.models import Wallet
from user.models import User
from history.models import History
import os
from dotenv import load_dotenv

load_dotenv()
stripe_key = os.getenv('STRIPE_BACKEND_ID')
stripe.api_key = stripe_key


class RechargeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        totalAmount = int(float(request.data['amount'])*100)
        stripe.Charge.create(
            source=request.data['token'],
            amount=totalAmount,
            currency="eur"
        )

        wallet = Wallet.objects.get(pk=request.user.wallet_id)
        wallet.balance = float(wallet.balance) + float(request.data['amount'])
        wallet.save()

        history = History(
            type='recharge',
            origin_user=self.request.user,
            target_user=self.request.user,
            amount=request.data['amount']
        )
        history.save()

        return Response('OK', status.HTTP_200_OK)


class SendMoneyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.get(pk=request.user.wallet_id)
        wallet.balance = float(wallet.balance) - float(request.data['amount'])
        wallet.save()

        user_dest = User.objects.get(pk=request.data['userId'])
        wallet_dest = Wallet.objects.get(pk=user_dest.wallet_id)
        wallet_dest.balance = float(
            wallet_dest.balance) + float(request.data['amount'])
        wallet_dest.save()

        history = History(
            type='send_money',
            origin_user=self.request.user,
            target_user=user_dest,
            amount=request.data['amount'],
            message=request.data['message']
        )
        history.save()

        return Response('OK', status=status.HTTP_200_OK)
