from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView

from tasks.forms import WorkerEditForm
from tasks.models import Worker


class HomePageView(TemplateView):
    template_name = 'tasks/home.html'


class ProfileView(DetailView):
    model = Worker
    template_name = 'tasks/my_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.id


class EditProfileView(UpdateView):
    model = Worker
    form_class = WorkerEditForm
    template_name = 'tasks/worker_form.html'
    success_url = reverse_lazy("tasks:profile")

    def get_object(self, queryset=None):
        return self.request.user
