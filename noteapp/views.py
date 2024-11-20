from noteapp.serializers import (
    NoteSerializer,
    UserSerializer,
    ProfileSerializer,
    RegisterSerializer,
    LoginSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from noteapp.models import Note, Profile
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta


# Create your views here.
@api_view(["POST"])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully"}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user_view(request):
    try:
        user = request.user
        password = request.data.get("password")

        if not password:
            return Response(
                {"error": "Password is required"},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()
        return Response(
            {"message": "User deleted successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        tokens = serializer.validated_data
        return Response(tokens, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_details_view(request):
    try:
        user = request.user
        serializer = UserSerializer(user)
        if request.method == "GET":
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    try:
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        if request.method == "GET":
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            if profile.image:
                profile.image = None
                profile.save()
                return Response(
                    {"message": "Profile deleted successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "No Profile pic found"}, status=status.HTTP_404_NOT_FOUND
            )
    except Profile.DoesNotExist:
        return Response(
            {"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"message": "Logout successfully"}, status=status.HTTP_205_RESET_CONTENT
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_notes_view(request):
    query = request.query_params.get("search")
    if not query:
        return Response(
            {"error": "Search query is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    notes = Note.objects.filter(
        Q(title__icontains=query)
        | Q(body__icontains=query)
        | Q(category__icontains=query),
        user=request.user,
    ).order_by("-updated_at")
    serializer = NoteSerializer(notes, many=True)
    if notes:
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "No notes found"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def notes_view(request):
    if request.method == "GET":
        notes = Note.objects.filter(user=request.user).order_by("-updated_at")
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def note_detail_view(request, slug):
    try:
        note = Note.objects.get(slug=slug)
    except Note.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

    if note.user != request.user:
        return Response(
            {"error": "Not authorized to access this note"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "GET":
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        note.delete()
        return Response(
            {"message": "Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    # Override the `get_token_expiry` method to set the expiration time
    def _get_token_expiry(self, user):
        return timezone.now() + timedelta(minutes=10)


@api_view(["POST"])
def send_password_reset_email_view(request):
    email = request.data.get("email")
    if not email:
        return JsonResponse(
            {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "User with this email does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{user.pk}/{token}"

    send_mail(
        subject="Password Reset Request",
        message=f"""
Click the link below to reset your NoteWorthy account password:

{reset_url}

This link will expire in 10 minutes. If you did not request this reset, please ignore this email.
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return JsonResponse(
        {"message": "Password reset email sent successfully"}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def validate_reset_token_view(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    # Create a token generator
    token_generator = PasswordResetTokenGenerator()

    # Check if the token is valid and not expired
    if not token_generator.check_token(user, token):
        return JsonResponse(
            {"error": "Token is invalid or expired."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # If the token is valid and not expired
    return JsonResponse({"detail": "Token is valid."}, status=status.HTTP_200_OK)


@api_view(["POST"])
def reset_password_view(request, uid, token):
    new_password = request.data.get("new_password")
    if not new_password:
        return JsonResponse(
            {"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    token_generator = PasswordResetTokenGenerator()
    if not token_generator.check_token(user, token):
        return JsonResponse(
            {"error": "Token is invalid or expired."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(new_password)
    user.save()
    return JsonResponse(
        {"detail": "Password reset successfully."}, status=status.HTTP_200_OK
    )


def health_check_view(request):
    return JsonResponse({"status": "OK"})
