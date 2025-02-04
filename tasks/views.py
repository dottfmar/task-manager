from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView, ListView

from tasks.forms import WorkerEditForm, TeamForm, ProjectForm
from tasks.models import Worker, Team, Project


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


class TeamView(ListView):
    model = Team
    template_name = 'tasks/teams.html'


class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("tasks:teams")


class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("tasks:teams")
    template_name = 'tasks/team_form.html'


class TeamDeleteView(DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:teams")
    template_name = 'tasks/team_delete.html'


class ProjectView(ListView):
    model = Project
    template_name = 'tasks/projects.html'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("tasks:projects")


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("tasks:projects")
    template_name = 'tasks/project_form.html'

class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:projects")

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'