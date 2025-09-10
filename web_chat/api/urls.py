from django.urls import path

from . import s3_views, views

urlpatterns = [
    path("custom_users", views.get_custom_user_details, name="custom_users"),
    path("user_contacts", views.get_user_contacts_details, name="user_contacts"),
    path("addContact", views.create_custom_user, name="addContact"),
    path("contactDetails", views.get_contacts_id_details, name="contacts"),
    path("s3/upload", s3_views.upload_to_s3, name="s3_upload"),
]
