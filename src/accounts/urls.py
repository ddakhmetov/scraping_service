from django.urls import path
from accounts.views import login_vew, logout_view, register_view, update_view, delete_view, contact

urlpatterns = [
    path('login/', login_vew, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('update/', update_view, name='update'),
    path('delete', delete_view, name='delete'),
    path('contact', contact, name='contact'),
]