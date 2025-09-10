from django.db import models

# Creating users model for API


class CustomUsersModel(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        db_table = "t_chat_users"
        managed = False

    def __str__(self):
        return self.email


class UserContactsModel(models.Model):
    contact_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUsersModel, on_delete=models.CASCADE, related_name="contacts"
    )
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=50, unique=True)
    mobile = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "t_user_contacts"
        managed = False

    def __str__(self):
        return self.username
