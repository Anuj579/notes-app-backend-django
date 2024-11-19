from django.urls import path
from noteapp.views import (
    notes_view,
    note_detail_view,
    search_notes_view,
    register_view,
    delete_user_view,
    login_view,
    user_details_view,
    profile_view,
    logout_view,
    health_check_view
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user-details/", user_details_view, name="user_profile"),
    path("profile/", profile_view, name="profile"),
    path("logout/", logout_view, name="logout"),
    path("delete-user/", delete_user_view, name="delete_user"),
    path("notes/", notes_view, name="notes"),
    path("notes/<slug:slug>/", note_detail_view, name="note_detail"),
    path("notes-search/", search_notes_view, name="notes-search"),
    path("health/", health_check_view, name="health-check"),
]
