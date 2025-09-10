import boto3
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def upload_to_s3(request):
    """Upload a file to S3 and return its URL"""
    try:
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=400)

        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        key = f"chat_files/{file_obj.name}"

        s3.upload_fileobj(file_obj, bucket, key)
        file_url = f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
        file_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=3600,  # URL valid for 1 hour
        )
        return Response({"file_url": file_url}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)
