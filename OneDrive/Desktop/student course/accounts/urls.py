from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('notification-preference/', views.notification_preference, name='notification_preference'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/test-coursera/', views.test_coursera_api, name='test_coursera_api'),
]