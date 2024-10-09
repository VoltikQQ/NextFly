from django.urls import path
from django.views.decorators.cache import cache_page

from shop import views


urlpatterns = [
    path('', views.ShopHome.as_view(), name='home'),
    path('shop/<slug:item_slug>/', views.ItemDetail.as_view(), name='item'),
    path('add_item', views.AddItem.as_view(), name='add_item'),
    path('category/<slug:cat_slug>/', views.ItemCategory.as_view(), name='category'),
    path('about', views.about, name='about'),
    path('vacancies', views.vacancies, name='vacancies'),
    path('contacts', views.contacts, name='contacts'),
    path('edit/<slug:slug>/', views.UpdateItem.as_view(), name='edit_item'),
    path('delete/<slug:slug>/', views.DeleteItem.as_view(), name='delete_item'),
    path('search', views.Search.as_view(), name='search'),
]
