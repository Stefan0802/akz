from tkinter.font import names

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('post_list/', views.list_post, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]