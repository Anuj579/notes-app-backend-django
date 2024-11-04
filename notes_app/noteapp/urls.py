from django.urls import path
from noteapp.views import (
    notes_view,
    note_detail_view,
    search_notes_view,
    register_view,
    login_view,
    get_user_profile_view,
    logout_view,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user-details/", get_user_profile_view, name="user_profile"),
    path("logout/", logout_view, name="logout"),
    path("notes/", notes_view, name="notes"),
    path("notes/<slug:slug>/", note_detail_view, name="note_detail"),
    path("notes-search/", search_notes_view, name="notes-search"),
]
