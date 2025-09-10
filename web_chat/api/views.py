from django.shortcuts import render
from loguru import logger
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CustomUsersModel, UserContactsModel
from .serializers import (
    AddContactsModelSerializer,
    CustomUsersModelSerializer,
    UserContactsModelSerializer,
)

# Create your views here.


@api_view(["GET"])
def get_custom_user_details(request):
    """API view to get custom user details"""
    if request.method == "GET":
        users = CustomUsersModel.objects.only(
            "user_id",
            "username",
            "email",
            "mobile",
        )
        serializer = CustomUsersModelSerializer(users, many=True)
        return Response(serializer.data)
    return Response({"error": "Invalid request method"}, status=400)


@api_view(["GET"])
def get_user_contacts_details(request):
    """API view to get custom user details"""
    if request.method == "GET":
        user_id = request.query_params.get("user_id")
        if user_id:
            users = UserContactsModel.objects.filter(user_id=user_id)
            serializer = UserContactsModelSerializer(users, many=True)
            if not serializer.data:
                return Response(
                    {"status": "failed", "error": "No contacts found for this user"},
                    status=404,
                )
            return Response(serializer.data)
        else:
            return Response({"error": "User ID not provided"}, status=400)
    return Response({"error": "Invalid request method"}, status=400)


@api_view(["GET"])
def get_contacts_id_details(request):
    """API view to get custom user details"""
    if request.method == "GET":
        contact_id = request.query_params.get("contact_id")
        if contact_id:
            users = UserContactsModel.objects.filter(contact_id=contact_id)
            serializer = UserContactsModelSerializer(users, many=True)
            if not serializer.data:
                return Response(
                    {"status": "failed", "error": "No contacts found for this user"},
                    status=404,
                )
            return Response(serializer.data)
        else:
            return Response({"error": "User ID not provided"}, status=400)
    return Response({"error": "Invalid request method"}, status=400)


@api_view(["POST"])
def create_custom_user(request):
    """API view to create a new custom user"""
    if request.method == "POST":
        logger.info(f"Request data: {request.data}")
        serializer = AddContactsModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    return Response({"error": "Invalid request method"}, status=400)
