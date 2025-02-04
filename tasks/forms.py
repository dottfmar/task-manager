from django import forms

from tasks.models import Worker


class WorkerEditForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            'first_name',
            'last_name',
            'email',
            'position'
        ]
