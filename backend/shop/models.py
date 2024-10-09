import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class SellManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(selling=1)


class Item(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Price")
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="Discount")
    description = models.TextField(blank=True, verbose_name="Description")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    selling = models.BooleanField(default=False, verbose_name="On sale")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, related_name='items', verbose_name="Category")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='items', null=True, default=None)
    photos = models.ManyToManyField('ItemImage', blank=True, related_name='photos')
    total_rating = models.IntegerField(default=0, verbose_name='Total rating')
    num_rating = models.IntegerField(default=0, verbose_name='Numer of ratings')
    avg_rating = models.FloatField(default=0, verbose_name='Average rating')

    objects = models.Manager()
    is_selling = SellManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item', kwargs={'item_slug': self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True).select_related('user')

    def calculate_avg_rating(self):
        self.avg_rating = self.total_rating / self.num_rating

    class Meta:
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Category")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'


class ItemImage(models.Model):
    photo = models.ImageField(upload_to='photos/', verbose_name="Photo")

    def __str__(self):
        return self.photo.url


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads-model')