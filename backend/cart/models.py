from keyword import kwlist

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from shop.models import Item


# Create your models here.
class PaymentHistory(models.Model):
    PENDING = "P"
    COMPLETED = "C"
    FAILED = "F"

    STATUS_CHOICES = (
        (PENDING, "pending"),
        (COMPLETED, "completed"),
        (FAILED, "failed"),
    )

    email = models.EmailField(unique=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment-{self.pk}-{self.item}-{self.user}-{self.payment_status}"

    class Meta:
        verbose_name = 'Payment history'
        verbose_name_plural = 'Payment histories'
        ordering = ['-id']