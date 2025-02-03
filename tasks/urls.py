from django.urls import path

from tasks.views import HomePageView

app_name = 'tasks'

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
]