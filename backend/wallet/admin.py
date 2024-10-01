from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from wallet.models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'balance']
    fieldsets = (
        ('Informacion basica', {
            'fields': ['balance']
        }),
    )
