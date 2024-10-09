from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from shop.models import Item


# Create your models here.
class Reviews(models.Model):
    text = models.TextField(blank=True, verbose_name="Commentary")
    rating = models.IntegerField(null=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='Parent',
                               on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text

    def get_review(self):
        return self.reviews_set.select_related('user').order_by('time_create')

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-time_create']