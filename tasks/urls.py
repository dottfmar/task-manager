from django.urls import path

from tasks.views import (
    HomePageView,
    ProfileView,
    EditProfileView,
    TeamView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView
)

app_name = 'tasks'

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit-profile"),
    path("teams/", TeamView.as_view(), name="teams"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
]