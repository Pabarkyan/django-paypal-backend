from django.db import models


class Wallet(models.Model):
    balance = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return str(self.id)
