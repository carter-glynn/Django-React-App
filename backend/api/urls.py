from django.urls import path
from . import views

urlpatterns = [
    path("items/", views.ItemListCreate.as_view(), name="item-list"),
    path("items/delete/<int:pk>/", views.ItemDelete.as_view(), name="delete-item"),
    path("reports/", views.GenerateReportView.as_view(), name="generate-report"),
    path('set-notification/', views.NotificationPreferenceView.as_view(), name='set-notification'),
    path('user/', views.CurrentUserView.as_view(), name='current_user'),
]