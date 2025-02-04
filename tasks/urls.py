from django.urls import path

from tasks.views import HomePageView, ProfileView, EditProfileView

app_name = 'tasks'

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit-profile"),
]