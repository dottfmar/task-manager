from django.urls import path

from tasks.views import (
    HomePageView,
    ProfileView,
    EditProfileView,
    TeamView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    ProjectView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    TaskView,
    TaskCreateView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView,
    TaskToggleStatusView,
    register,
)

app_name = "tasks"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", EditProfileView.as_view(), name="edit-profile"),
    path("teams/", TeamView.as_view(), name="teams"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    path("projects/", ProjectView.as_view(), name="projects"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path(
        "projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"
    ),
    path(
        "projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"
    ),
    path("tasks/", TaskView.as_view(), name="tasks"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "toggle-status/<int:pk>/",
        TaskToggleStatusView.as_view(),
        name="task-toggle-status",
    ),
    path("accounts/register/", register, name="register"),
]
