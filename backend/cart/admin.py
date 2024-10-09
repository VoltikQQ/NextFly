from django.contrib import admin

from cart.models import PaymentHistory


# Register your models here.
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'item', 'payment_status', 'created_at', 'updated_at')
    list_display_links = ('id',)
    search_fields = ('item',)


admin.site.register(PaymentHistory, PaymentHistoryAdmin)