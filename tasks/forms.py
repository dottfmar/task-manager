from django import forms
from django.contrib.auth import get_user_model

from tasks.models import Worker, Team


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
