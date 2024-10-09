from django.contrib import admin

from recommend.models import Reviews


# Register your models here.
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'time_create', 'item', 'parent')
    list_display_links = ('id', 'item')
    search_fields = ('item_id',)

admin.site.register(Reviews, ReviewsAdmin)