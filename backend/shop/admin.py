from django.contrib import admin
from .models import Item, Category


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'selling', 'time_create', 'category', 'brief_info')
    list_display_links = ('id', 'title')
    ordering = ['time_create', 'title']
    search_fields = ('title', 'description', 'category__name')
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ('selling',)
    list_filter = ('selling', 'category')
    actions = ['unpublish', 'publish']
    fields = ['title', 'slug', 'price', 'description', 'category', 'total_rating', 'num_rating', 'avg_rating']

    @admin.display(description='Brief description', ordering='description')
    def brief_info(self, item: Item):
        return f"Description: {len(item.description)} characters"

    @admin.action(description='Unpublish selected items for sale')
    def unpublish(self, request, queryset):
        row_update = queryset.update(selling=False)
        if row_update == 1:
            message_bit = '1 entry updated'
        else:
            message_bit = f'{row_update}entries updated'
        self.message_user(request, f"{message_bit}")

    @admin.action(description='Publish selected items for sale')
    def publish(self, request, queryset):
        row_update = queryset.update(selling=True)
        if row_update == 1:
            message_bit = '1 entry updated'
        else:
            message_bit = f'{row_update} entries updated'
        self.message_user(request, f"{message_bit}")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'item', 'payment_status', 'created_at', 'updated_at')
    list_display_links = ('id',)
    search_fields = ('item',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Reviews, ReviewsAdmin)

