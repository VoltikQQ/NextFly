from django.urls import path
from recommend import views

app_name = 'recommend'

urlpatterns = [
    path('add-review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('delete-review/<int:item_id>/<int:review_id>/', views.delete_review, name='delete_review'),
]
