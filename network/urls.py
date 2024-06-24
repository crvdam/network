
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:page>", views.index, name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("add_follow/<int:user_id>", views.add_follow, name="add_follow"),
    path("remove_follow/<int:user_id>", views.remove_follow, name="remove_follow"),
    path("like", views.like, name="like"),
    path("edit_post", views.edit_post, name="edit_post"),
]
