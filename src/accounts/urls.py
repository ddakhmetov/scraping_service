from django.urls import path
from accounts.views import login_vew, logout_view, register_view

urlpatterns = [
    path('login/', login_vew, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]