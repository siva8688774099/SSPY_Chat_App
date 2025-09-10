from rest_framework.serializers import ModelSerializer

from .models import CustomUsersModel, UserContactsModel


class CustomUsersModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUsersModel
        fields = ("user_id", "username", "email", "mobile")


class UserContactsModelSerializer(ModelSerializer):
    class Meta:
        model = UserContactsModel
        fields = ["contact_id", "username", "email", "mobile", "user"]


class AddContactsModelSerializer(ModelSerializer):
    class Meta:
        model = UserContactsModel
        fields = ["contact_id", "username", "email", "mobile", "user"]
