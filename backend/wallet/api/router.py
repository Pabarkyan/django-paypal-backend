from django.urls import path
from wallet.api.views import RechargeView, SendMoneyView

urlpatterns = [
    path('wallet/recharge/', RechargeView.as_view()),
    path('wallet/send_money/', SendMoneyView.as_view())
]