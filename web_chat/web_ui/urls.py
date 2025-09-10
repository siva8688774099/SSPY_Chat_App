from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_login, name="login_user"),
    path("reset_password", views.reset_password, name="password_reset"),
    path("register", views.create_user, name="register"),
    path("reset_password", views.reset_password, name="password_reset"),
    path("password_reset_mail", views.password_reset_mail, name="password_reset_mail"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    path("home", views.home, name="home"),
    path("chat", views.user_chat, name="chat"),
    path("add_contact", views.add_contact, name="add_contact"),
    path("user/<int:user_id>/", views.message, name="message"),
]
