from django.urls import path
from accounts.views import logout_view, login_view, register_view, profile_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register_done/', login_view, name='register_done'),
    path('profile_page/', profile_view, name='profile_page'),
]