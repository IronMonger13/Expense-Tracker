from django.contrib import admin
from tracker.models import *


class Transaction_Admin(admin.ModelAdmin):
    list_display = (
        "title",
        "amount",
        "transaction_date",
        "transaction_type",
        "created_on",
    )
    list_filter = ("category",)


# Register your models here.
admin.site.register(Transaction, Transaction_Admin)
