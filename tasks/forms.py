from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Worker, Team, Project


class WorkerEditForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            'first_name',
            'last_name',
            'email',
            'position'
        ]


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'members']

    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "team"]

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "cols": 40,
                "class": "form-control-lg form-control-fixed"
            }),
        required=False,
        help_text="Enter a detailed description of the project"
    )
    team =  forms.ModelChoiceField(
        queryset=Team.objects.all(),
        widget=forms.RadioSelect(
            attrs={"class": "form-check-input"}
        ),
        required=True
    )
