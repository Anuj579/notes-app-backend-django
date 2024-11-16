from rest_framework import serializers
from .models import Note, Profile
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "title", "body", "slug", "category", "created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "date_joined"]
        extra_kwargs = {
            "email": {"read_only": True},
            "date_joined": {"read_only": True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    image_url = (
        serializers.SerializerMethodField()
    )  # Calls a custom method to get data for this field, not directly from the model

    class Meta:
        model = Profile
        fields = ["user", "image", "image_url"]
        read_only_fields = ["user"]

    def get_image_url(self, obj):
        if obj.image:  # Checks if an image exists
            return obj.image.url  # Generates the full URL
        return None  # Return empty string instead of None for consistency


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if User.objects.filter(email=validated_data["email"]).exists():
            raise serializers.ValidationError({"message": "Email already exists"})

        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
