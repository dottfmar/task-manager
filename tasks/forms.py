from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from tasks.models import Worker, Team, Project, TaskType, Task, Position


class WorkerEditForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ["first_name", "last_name", "email", "position"]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "members"]

    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "team"]

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 4, "cols": 40, "class": "form-control-lg form-control-fixed"}
        ),
        required=False,
        help_text="Enter a detailed description of the project",
    )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        required=True,
    )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "project",
            "assignees",
            "is_completed",
        ]

    priority = forms.ChoiceField(choices=Task.PriorityChoices, widget=forms.RadioSelect)

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(), required=False, empty_label="Select Task Type"
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(), required=False, empty_label="Select Project"
    )

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    widgets = {
        "name": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter task name"}
        ),
        "description": forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Task description"}
        ),
        "deadline": forms.DateTimeInput(
            attrs={"class": "form-control", "placeholder": "Deadline"}
        ),
        "priority": forms.RadioSelect(attrs={"class": "form-check-input"}),
        "task_type": forms.RadioSelect,
        "project": forms.Select(attrs={"class": "form-control"}),
        "assignees": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    }


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = ["username", "password1", "password2", "position"]

    position = forms.ModelChoiceField(
        queryset=Position.objects.all(), required=False, empty_label="Select Position"
    )
