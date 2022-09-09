
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('savePost', views.savePost, name='savePost'),
    path('profile/<str:username>', views.userProfile, name='profile'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unFollow, name='unfollow'),
    path('followingPosts', views.followingPosts, name='followingPosts'),
    path('edit/<int:post_id>', views.editPost, name='editPost'),
    path('like/<int:post_id>', views.postLiked, name='postLiked')
]
