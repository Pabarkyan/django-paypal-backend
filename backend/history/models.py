from django.db import models


class History(models.Model):
    HistoryType = (
        ('recharge', 'recharge'),
        ('send_money', 'send_money')
    )

    type = models.CharField(max_length=255, choices=HistoryType)
    target_user = models.ForeignKey('user.User', related_name='target_user', null=True, blank=True, on_delete=models.SET_NULL)
    origin_user = models.ForeignKey('user.User', related_name='origin_user', null=True, blank=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=100, decimal_places=2)
    message = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)