from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
    ListView,
)

from tasks.forms import (
    WorkerEditForm,
    TeamForm,
    ProjectForm,
    TaskForm,
    WorkerCreationForm,
)
from tasks.models import Worker, Team, Project, Task


class HomePageView(TemplateView):
    template_name = "tasks/home.html"


class ProfileView(LoginRequiredMixin, DetailView):
    model = Worker
    template_name = "tasks/my_profile.html"

    def get_object(self, queryset=None):
        return self.request.user.id


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Worker
    form_class = WorkerEditForm
    template_name = "tasks/worker_form.html"
    success_url = reverse_lazy("tasks:profile")

    def get_object(self, queryset=None):
        return self.request.user


class TeamView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "tasks/teams.html"
    paginate_by = 10


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("tasks:teams")


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model = Team
    form_class = TeamForm
    success_url = reverse_lazy("tasks:teams")
    template_name = "tasks/team_form.html"


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    success_url = reverse_lazy("tasks:teams")
    template_name = "tasks/team_delete.html"


class ProjectView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "tasks/projects.html"
    paginate_by = 10


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("tasks:projects")


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy("tasks:projects")
    template_name = "tasks/project_form.html"


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy("tasks:projects")
    template_name = "tasks/project_delete.html"


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "tasks/project_detail.html"


class TaskView(LoginRequiredMixin, ListView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/tasks.html"
    success_url = reverse_lazy("tasks:tasks")
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        completed = self.request.GET.get("completed")
        if completed is not None:
            if completed.lower() == "true":
                queryset = queryset.filter(is_completed=True)
            elif completed.lower() == "false":
                queryset = queryset.filter(is_completed=False)
        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)
        return queryset


class TaskToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()
        next_url = request.POST.get(
            "next", request.META.get("HTTP_REFERER", "tasks:tasks")
        )
        return redirect(next_url)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:tasks")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workers"] = Worker.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:tasks")
    template_name = "tasks/task_form.html"

    def form_valid(self, form):
        task = form.save(commit=False)
        task.is_completed = form.cleaned_data.get("is_completed", False)
        task.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workers"] = Worker.objects.all()
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:tasks")
    template_name = "tasks/task_delete.html"


def register(request):
    if request.method == "POST":
        form = WorkerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tasks:home")
    else:
        form = WorkerCreationForm()
    return render(request, "registration/register.html", {"form": form})
